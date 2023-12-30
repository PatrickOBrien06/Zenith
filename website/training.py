from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for
from .models import User, Schedule, Exercise, Set
from . import db 
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Blueprint development
training = Blueprint("training", __name__, template_folder="templates")

# Home / Dashboard layout 
@training.route("/", methods=['POST', 'GET'])
@training.route("/home", methods=['POST', 'GET'])
@login_required
def home():
    schedules = Schedule.query.filter_by(user_id=current_user.id).all()
    exercises = Exercise.query.filter_by(user_id=current_user.id).all()
    sets = Set.query.filter_by(user_id=current_user.id)

    return render_template("index.html", schedules=schedules, exercises=exercises, sets=sets)

# Create Schedule
@training.route("/create_schedule", methods=["POST", "GET"])
@login_required
def create_schedule():
    if request.method == "POST":
        schedule_name = request.form.get("schedule_name")
        exercise_name = request.form.get("exercise_name")
        set_weight = request.form.get("set_weight")
        set_reps = request.form.get("set_reps")
        
        user = User.query.filter_by(email=current_user.email).first()

        schedule = Schedule(schedule_name=schedule_name, user_id=user.id, date_created=datetime.utcnow())
        db.session.add(schedule)
        db.session.commit()

        exercise = Exercise(exercise_name=exercise_name, schedule_id=schedule.id, user_id=user.id)
        db.session.add(exercise)
        db.session.commit()

        set_data = Set(reps=int(set_reps), weight=float(set_weight), exercise_id=exercise.id, user_id=user.id)
        db.session.add(set_data)
        db.session.commit()

    return render_template("create_schedule.html")