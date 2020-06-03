from flask import Flask, request, current_app, redirect, url_for
from .config import Config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, user_logged_in
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_security import Security

import os
import babel

db = MongoEngine()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

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
