from flask import Flask,render_template,request,session,url_for,flash,redirect,logging,make_response
from FireBlog import insert,fetch,checkuser,fetcharticles,insertarticle,fetchuserarticles,fetcharticlebyid,deletearticle
from passlib.hash import sha256_crypt
from wtforms import Form,StringField,PasswordField,validators
from FireBlog.users.forms import Register,Article
from functools import wraps

app.register_blueprint(FireBlog)

app=Flask(__name__)
app.config['SECRET_KEY'] = 'therandomstring'

#main route
@app.route('/')
def index():
    return render_template('home.html')


#about route
@app.route('/aboutus')
def about():
    return render_template('about.html')




#REgister page
@app.route('/register',methods=['GET','POST'])
def register():
    form=Register(request.form)
    if request.method =='POST' and form.validate():
        name=form.name.data
        email=form.email.data
        username=form.username.data
        if checkuser(username,email):
            flash('username taken ','danger')
            return redirect(url_for('register'))
        else:
            password=sha256_crypt.encrypt(form.password.data)
            insert(name,email,username,password)
            flash('You are registerd','success')
            return redirect(url_for('index'))
    

    return render_template('register.html',form=form)



#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        data= fetch(username)
        if data==False:
            #username not found
            flash('Username not found','danger')
            return redirect(url_for('login'))
        else:
            #username found
            if sha256_crypt.verify(password_candidate,data['password']):
                #Password Matched
                flash('You are loggedin','success')
                session['username']=data['username']
                session['loggedin']=True

                return redirect(url_for('dashboard'))
            else:
                #Password did not match
                flash('Password did not match','danger')
                return redirect(url_for('login'))
            
    return render_template('login.html')
# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
#logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('you are logged out','success')
    return redirect(url_for('login'))
#DAshboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
        articles=fetchuserarticles(session['username'])
        return render_template('dashboard.html',articles=articles)
#articles
@app.route('/articles')
def articles():
    articles=fetcharticles()
    return render_template('articles.html',articles=articles)
#single article
@app.route('/article/<string:id>/')
def article(id):
    data=fetcharticlebyid(id)
    return render_template('article.html',article=data)
#addingarticles 
@app.route('/add_articles',methods=['POST','GET'])
@is_logged_in
def addarticles():
    form=Article(request.form)
    if request.method =='POST' and form.validate():
        title=form.title.data
        body=form.body.data
        #insertfunctionforarticles
        insertarticle(title,body,session['username'])
        flash('Article Created', 'success')
        return redirect(url_for('dashboard'))


    return render_template('addarticle.html',form=form)

#DELETE article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    deletearticle(id)
    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))



#running the APP
if __name__ =='__main__':
    
    app.run(debug=True)
