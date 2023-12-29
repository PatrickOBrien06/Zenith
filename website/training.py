from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for
from .models import User, Schedule, Exercise, Set
from . import db 
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Blueprint development
training = Blueprint("training", __name__, template_folder="templates")

# Home / Dashboard layout 
@training.route("/", methods=['POST', 'GET'])
@training.route("/home", methods=['POST', 'GET'])
@login_required
def home():
    exercise = 0
    weight = 0
    reps = 0
    if request.method == "POST":
        exercise = request.form.get('exercise')
        weight = request.form.get('weight')
        reps = request.form.get('reps')
        
    return render_template("index.html", exercise=exercise, weight=weight, reps=reps)

# Create Schedule
@training.route("/create_schedule", methods=["POST", "GET"])
def create_schedule():
    return render_template("add_exercise.html")