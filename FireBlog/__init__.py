import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from FireBlog.users.models import User,Article



########KEY##########

key={
  "type": "service_account",
  "project_id": os.environ.get('PROJECT_ID'),
  "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDdJpd0G51h/wCq\nbqZ0HF4/S+eH3jVP2WN2XELYEMYo2IeapkYMfmuKULXABMV8dWaOavB9HQ/Wltr8\nWvnAkIkHL65bt7PJLS1zQEv9Jjv8FJMFP3ZV1rdZzhMjP0rPsq7rayp8Uu6EChLe\nsNYuJPYMicACupE7cF/sfLorRMwc2/vJzBSQxEDS15mufJGojicbqPyRpkEN5rtj\n/gd6ZM6UuFUIUCFj57ZwfznLXDKhrMIwfY6qphrYWDGeDjGExLPxwLErCx8o9T3P\n2BJitiifZ+hzUCb66/Nw4dnXwKAk7oDNG70dfBwh6K8bsXKlDd8bXh2T0tagVtOo\nT0abkYlXAgMBAAECggEAIhF/43Mdm6sc/yRsoBZ+rmGTGWsx60sh92nfIknzPPee\nbESRJfuTtYsZdKtHgRTU57uxsJR5jCVRNu8M6o1ZjrHZumdiWuuKxOZyzlzFgN/q\nhjRwlmitdjg42oU1kSmFqN6pfN2JwO2MWqIDXLh07xmJauIy3WVCYbwVMfU3PHqd\nzwbYms8Jd0JPzk9WniODMcLTfbelm54qVd3GV5d3JGSHoB/JiTuG+J3Lm5WzrUQo\nntv6qhjVQfYLomwyk2sfNuFMBbfQgtuVF0jmwwsidSeFXNX580gygcVBBtEPfeH1\n7Ya9rq5txd6tSX1PwYbH9iXNICNY3vXTxGxkuEhDgQKBgQDwQRELS1ZITdUPm0PA\nyFOMInP6+DU9+vACwljHGAWKWfOjA354igCzJfdUCIrOfHENaXInXJnf3RPI8Xqv\nQNQoLNdQ7vthYviw/IFxtyh/8SfnVk9csah7fibwFhjQQyovEc1mSvdvBSl+Ycp4\nPDq1ST4VGvWLvQ1stJqnwJwVlQKBgQDrpQMO6Lwp2yBh5P5E+LhXFkPiWKbi8Mnx\nU/M+ODwAlPHUYsEvuOlxIdbnJV8AREYa8E9SDduP5+mXhW4Opi29nsMqgO8gfq50\nATvmjeOHZ89beZ8/tLiSEPYTPO/eG77yz0UhIbq5lIUYLUJu4FeWoK+R2wh5fEVG\npC7pYvJQOwKBgAVKOXjZMM4owI82aPh+sLA+NfWJr4ps0woMg23mzoBsWJv3QLqg\nt0E6jcaQ5ZWEUezsrHHHbS/rqzrabkwbjlBQJHGIwYo0Zqtm8+awFLk0cx953Ad7\nde06KttQcT1srSoaJz6gWfBc2bwJpS6ejOBe+3n1fQCVqg0BsQIOkKE9AoGAM0Bq\nj92Sv0/HlUMnAn1OKrLPBPXfJlDUu0ZVC11Tv5SlnFn2RpjjPRXtFc0NApPW45kM\nx334GS6JockFjO4b2LglHqN4XwruipCSJK0LpbGwaebj+gkmc654tup0CUzjlQ/7\nqx8Y67Af2ohNgKwOoNZGGWUYTMP4lUq0YVKB/W0CgYB1gE8Y2Yah58WNtbFRkufK\npBI94glsV3Jf5l771bRxZUfQfooX4FmFaFpdxnV5WYWcU8w2IH09F22lPUcTJ+yP\nMoKYZAcbuPyADFPEXLh3repsmCJfWM55PxDPBAj8JCgxgcgxHbBorihAhotjlkuq\nNPIpg9fSb+3DvrYYK+9hPQ==\n-----END PRIVATE KEY-----\n",
  "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
  "client_id": os.environ.get('CLIENT_ID'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ajbgb%40fireblog-60ee6.iam.gserviceaccount.com"
}
######################


cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred)
db = firestore.client()
user_ref = db.collection(u'users')
articles_ref=db.collection(u'articles')



def insert(name,email,username,hashpass): #function for inserting to DB
  user = User(name,email,username,hashpass)
  user_ref.document(username).set(user.todict())
def fetch(username):
    doc = user_ref.document(username).get()
    if doc.exists:
        doc=doc.to_dict()
        return doc
    else:
        return False
def checkuser(username,email):
  doc = user_ref.document(username).get()
  if doc.exists:
    return True
  else:
    return False

def fetcharticles():
  data={}
  docs=articles_ref.stream()
  for doc in docs:
    data[doc.id] =doc.to_dict()
  return data
def insertarticle(title,body,username):
  article=Article(title,body,username)
  articles_ref.document().set(article.todict())
def fetchuserarticles(username):
  data={}
  docs=articles_ref.where(u'author',u'==',username).get()
  for doc in docs:
    data[doc.id] =doc.to_dict()
  return data
def fetcharticlebyid(id):
  doc=articles_ref.document(id).get()
  if doc.exists:
      doc=doc.to_dict()
      return doc
  else:
      return False
def deletearticle(id):
  articles_ref.document(id).delete()




