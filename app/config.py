import os

class Config(object):
    SECRET_KEY = "mega_super_secret_key"
    MONGOALCHEMY_DATABASE = 'db'
    MONGOALCHEMY_SERVER = 'mongodb'
    MONGOALCHEMY_PORT = '27017'
    MONGOALCHEMY_CONNECTION_STRING = "mongodb://mongodb:27017/db"
    FLASK_DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    JSONIFY_PRETTYPRINT_REGULAR = True
