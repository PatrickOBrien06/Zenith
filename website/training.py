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

    # Filter for rendering in home page
    schedules = Schedule.query.filter_by(user_id=current_user.id).all()
    exercises = Exercise.query.filter_by(user_id=current_user.id).all()
    sets = Set.query.filter_by(user_id=current_user.id).all()

    return render_template("index.html", schedules=schedules, exercises=exercises, sets=sets, current_user=current_user)


# Create Schedule
@training.route("/create_schedule", methods=["POST", "GET"])
@login_required
def create_schedule():
    if request.method == "POST":
        schedule_name = request.form.get("schedule_name")
        exercise_names = request.form.getlist("exercise_name[]")
        
        schedule = Schedule(schedule_name=schedule_name, user_id=current_user.id)
        db.session.add(schedule)
        db.session.commit()

        exerciseCounter = 1

        # Loop for exercise_name to be used to grab all set data
        for exercise_name in exercise_names:
            exercise = Exercise(exercise_name=exercise_name, schedule_id=schedule.id, user_id=current_user.id)
            db.session.add(exercise)
            db.session.commit()

            sets_weight = request.form.getlist(f"set_weight_{exerciseCounter}[]")
            sets_reps = request.form.getlist(f"set_reps_{exerciseCounter}[]")

            exerciseCounter += 1

            # Loop through sets_weight, grabbing the value for each and grabbing the corrosponding set_reps
            for setCounter in range(len(sets_weight)):
                set_weight = sets_weight[setCounter]
                set_reps = sets_reps[setCounter]
                set = Set(reps=set_reps, weight=set_weight, exercise_id=exercise.id, user_id=current_user.id)
                db.session.add(set)
                db.session.commit()

    return render_template("create_schedule.html")