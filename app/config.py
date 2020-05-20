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
