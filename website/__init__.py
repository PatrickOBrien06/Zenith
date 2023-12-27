from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db = SQLAlchemy()
    db.init_app(app)

    from .auth import auth

    app.register_blueprint(auth)

    from .models import User

    create_database(app)

    return app

def create_database(app):
    with app.app_context():
        db.create_all()