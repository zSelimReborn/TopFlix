import os

class Config(object):
    SECRET_KEY = "mega_super_secret_key"
    #MONGOALCHEMY_DATABASE = 'db'
    #MONGOALCHEMY_SERVER = 'mongodb'
    #MONGOALCHEMY_PORT = '27017'
    #MONGOALCHEMY_CONNECTION_STRING = "mongodb://mongodb:27017/db"
    MONGODB_DB = 'db'
    MONGODB_HOST = "mongodb"
    MONGODB_PORT = 27017
    #MONGODB_USERNAME = os.environ.get("DB_USER")
    #MONGODB_PASSWORD = os.environ.get("DB_PASS")
    FLASK_DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    JSONIFY_PRETTYPRINT_REGULAR = True

    FACEBOOK_OAUTH_CLIENT_ID = os.environ.get("FB_APP_ID")
    FACEBOOK_OAUTH_CLIENT_SECRET = os.environ.get("FB_SECRET_KEY")

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = False
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = [os.environ.get("MAIL_ADMIN")]