class User(object):
    def __init__(self,name,email,username,password):
        self.name=name
        self.email=email
        self.username=username
        self.password=password
    def todict(self):
        return self.__dict__
class Article(object):
    def __init__(self,title,body,username):
        self.author=username
        self.body=body
        self.title=title
    def todict(self):
        return self.__dict__