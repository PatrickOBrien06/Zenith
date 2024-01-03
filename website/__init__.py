from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()

db = SQLAlchemy()

def create_app():

    # App Configure
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config['SECRET_KEY'] = 'mbgodbnfvojvnseofefqwdqwifgbjdfsnf'
    db.init_app(app)

    # Blueprint Setup
    from .auth import auth

    app.register_blueprint(auth)

    from .training import training

    app.register_blueprint(training)

    from .models import User

    create_database(app)

    # Login Manager Setup
    login_manager.login_view = "auth.login"
    login_manager.login_message = "You must be signed in to reach this page!"
    login_manager.login_message_category = "danger"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    with app.app_context():
        db.create_all()