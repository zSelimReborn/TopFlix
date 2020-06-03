from flask import escape, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import jwt
from app import db, login

class User(UserMixin, db.Document):
    first_name      = db.StringField()
    last_name       = db.StringField()
    password        = db.StringField()
    email           = db.StringField()
    avatar          = db.StringField()
    titles_liked    = db.ListField(db.ReferenceField('Title'))
    titles_disliked = db.ListField(db.ReferenceField('Title'))
    genres_liked    = db.ListField(db.ReferenceField('Genre'))
    
    meta = {'collection': 'User'}

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str((self.id))   

    def fullname(self):
        return self.first_name + " " + self.last_name
    
    ''' se il parametro like è True allora è un like altrimenti un dislike '''
    def manage_titles(self, title, like=True):
        
        if like == True:
            if self.has_liked_title(title):
                self.update(pull__titles_liked=title)
            else:
                self.update(pull__titles_disliked=title)
                self.titles_liked.append(title)
        else:
            if self.has_disliked_title(title):
                self.update(pull__titles_disliked=title)
            else:
                self.update(pull__titles_liked=title)
                self.titles_disliked.append(title)
        
        self.save()
        
    def search_titles_disliked(self, title):
        for t in self.titles_disliked:
            if t.id == title.id:
                return t
        
        return None

    def has_disliked_title(self, title):
        return (self.search_titles_disliked(title) != None)
        
    def search_titles_liked(self, title):
        for t in self.titles_liked:
            if t.id == title.id:
                return t
        
        return None
    
    def has_liked_title(self, title):
        return (self.search_titles_liked(title) != None)

    @staticmethod
    def register(form):
        email = form.email.data
        if User.get_by_email(email) is not None:
            raise Exception("Email già registrata")


        nUser = User()

        nUser.first_name = form.first_name.data
        nUser.last_name = form.last_name.data
        nUser.email = form.email.data
        nUser.set_password(form.password.data)
        nUser.about_me = ""

        nUser.save()
        return nUser

    @staticmethod
    def login(email, password):
        user = User.get_by_email(email)
        if user is None:
            raise Exception("Email non registrata")
        
        if password.strip() == "":
            raise Exception("Password non inserita")

        if not user.check_password(password):
            raise Exception("Password errata")

        return user
    
    @staticmethod
    def facebook_login(email, fullname):
        user = User.get_by_email(email)
        if user is None:
            names = fullname.split()
            user = User(
                first_name=names[0],
                last_name=names[len(names)-1],
                email=email
            )

            user.save()
        
        return user

    @staticmethod
    def get_by_email(email):
        return User.objects.filter(email=email).first()        

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.get_id(), 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
        
    @staticmethod
    def get_by_id(id):
        return User.objects.get(id=id)

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.get_by_id(id)

@login.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)