from wtforms import StringField,Form,validators,PasswordField,TextAreaField
# Registration form
class Register(Form):
    name=StringField('Name',[validators.length(min=2,max=50)])
    username=StringField('Username',[validators.length(min=2,max=20)])
    email=StringField('Email',[validators.length(min=6,max=20)])
    password=PasswordField('Password',[validators.data_required(),validators.equal_to('confirm',message='PASSWORDS DONT MATCH')])
    confirm=PasswordField('Confirm Password')

class Article(Form):
    title=StringField('Title',[validators.length(min=2,max=200)])
    body=TextAreaField('Body',[validators.length(min=2,max=200)])
   

