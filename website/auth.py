from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for
from .models import User
from . import db 
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import secrets, string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from dotenv import load_dotenv

# Blueprint development
auth = Blueprint("auth", __name__, template_folder="templates")
load_dotenv()

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

# Password Recovery
@auth.route("/recovery", methods=["POST", "GET"])
def recovery():
    if request.method == 'POST':

        # Code generation  
        alphabet = string.ascii_letters + string.digits
        generated_code = ''.join(secrets.choice(alphabet) for i in range(6))
        print(generated_code)

        subject = "Password Reset"
        body = f'Code is {generated_code}'
        to_email = "pobrien66_s@nlesd.ca"
        outlook_username = os.getenv('outlook_username')
        outlook_password = os.getenv('outlook_password')

        # Set up the MIME
        message = MIMEMultipart()
        message["From"] = outlook_username
        message["To"] = to_email
        message["Subject"] = subject

        # Attach the body to the email
        print("Attaching")
        message.attach(MIMEText(body, "plain"))

        # Connect to the Outlook SMTP server
        print("Connecting")
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            print("Connected!")
            
            # Start TLS Encryption for security
            print("Starting TLS")
            server.starttls()

            # Log in to the SMTP server
            print("Logging In")
            server.login(outlook_username, outlook_password)

            # Send the email
            print("Sending")
            server.sendmail(outlook_username, to_email, message.as_string())

        # Confirmation
        print("Email sent successfully.")

    return render_template("password_recovery.html")