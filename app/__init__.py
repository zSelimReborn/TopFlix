from flask import Flask, request, current_app, redirect, url_for
from .config import Config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, user_logged_in
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_security import Security
#from flask_socketio import SocketIO

import os
import babel

''' Import per gestire task in background '''
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

db = MongoEngine()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()
mail = Mail()
scheduler = BackgroundScheduler()
#socketio = SocketIO()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mail.init_app(app)
    db.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)
    #socketio.init_app(app, logger=True, engineio_logger=True, cors_allowed_origins="*")

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.contact import bp as contact_bp
    app.register_blueprint(contact_bp, url_prefix='/contact')

    #from app.main.tasks import process_netflix_api
    #scheduler.add_job(func=process_netflix_api, trigger="cron", hour='00', minute='00', second='00')

    #scheduler.start()
    #atexit.register(lambda: scheduler.shutdown())

    @app.before_first_request
    def insert_genre_survey():
        from app.main.models import Survey

        surveys = Survey.objects()
        genre_survey = Survey(
            unique_key="genre_liked_survey",
            template_path="survey/genre.html",
            mandatory=True,
        )

        try:
            genre_survey.save()
        except:
            pass


    return app


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_debugger=True)
    #socketio.run(app, cors_allowed_origins="*")
