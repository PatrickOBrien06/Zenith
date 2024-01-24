from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for
from .models import User, Schedule, Exercise, Set
from . import db 
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Blueprint development
auth = Blueprint("auth", __name__, template_folder="templates")

# Signup page 
@auth.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Error handling
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash("Email already exists!", "danger")

        elif password1 != password2:
            flash("Password do not match!", "danger")

        # User creation
        else:
            password_hash = generate_password_hash(password1, method='pbkdf2')
            user = User(email=email, username=username, password=password_hash)
            session[email] = password_hash
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            flash("User created!", "success")
            return redirect(url_for("training.home"))

    return render_template("signup.html")

# Login page 
@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # User checking
        if user:
            if check_password_hash(user.password, password):
                flash("Signed In!", "success")
                login_user(user, remember=True)
                return redirect(url_for("training.home"))
            
            # Error handling
            else:
                flash("Invalid email or password!", "danger")
        else:
            flash("Invalid email or password!", "danger")

    return render_template("login.html")

# Logout user
@auth.route("/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for("auth.login"))