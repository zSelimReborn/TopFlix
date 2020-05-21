from flask import escape, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import jwt
from app import db, login

class User(UserMixin, db.Document):
    first_name  = db.StringField()
    last_name   = db.StringField()
    password    = db.StringField()
    email       = db.StringField()
    avatar      = db.StringField()
    
    meta = {'collection': 'User'}

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str((self.id))

    @staticmethod
    def register(form):
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
        
        if not user.check_password(password):
            raise Exception("Password errata")

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