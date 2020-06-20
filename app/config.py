import os

class Config(object):
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

    MONGODB_DATABASE = os.environ.get("MONGODB_DB")
    #MONGODB_HOST = os.environ.get("MONGODB_HOST")
    #MONGODB_PORT = int(os.environ.get("MONGODB_PORT") or 27017)
    #MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME")
    #MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
    MONGODB_URI = os.environ.get("MONGODB_URI")
    MONGO_CONNECT=False

    MONGODB_SETTINGS = {
        "DB": MONGODB_DATABASE,
        "host": MONGODB_URI,
        "connect": False
    }

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