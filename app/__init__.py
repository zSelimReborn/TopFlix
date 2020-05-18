from flask import Flask, request, current_app
from .config import Config
from flask_mongoalchemy import MongoAlchemy

db = MongoAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_debugger=True)
