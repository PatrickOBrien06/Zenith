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
    sets = Set.query.filter_by(user_id=current_user.id).all()
    
    setx = Set.query.all()

    for set in setx:
        print(set.weight)
        print(set.reps)

    return render_template("index.html", schedules=schedules, exercises=exercises, sets=sets, current_user=current_user)


# Create Schedule
@training.route("/create_schedule", methods=["POST", "GET"])
@login_required
def create_schedule():
    if request.method == "POST":
        schedule_name = request.form.get("schedule_name")
        exercise_names = request.form.getlist("exercise_name[]")
        sets_weight = request.form.getlist("set_weight[]")
        sets_reps = request.form.getlist("set_reps[]")
        
        schedule = Schedule(schedule_name=schedule_name, date_created=datetime.utcnow(), user_id=current_user.id)
        db.session.add(schedule)
        db.session.commit()

        # Loop through each exercise
        for index, exercise_name in enumerate(exercise_names):
            exercise = Exercise(exercise_name=exercise_name, schedule_id=schedule.id, user_id=current_user.id)
            db.session.add(exercise)
            db.session.commit()

            # Extract sets for the current exercise based on index and the total number of exercises
            sets_per_exercise = len(sets_weight) // len(exercise_names)
            sets_start = index * sets_per_exercise
            sets_end = sets_start + sets_per_exercise
            exercise_sets_weight = sets_weight[sets_start:sets_end]
            exercise_sets_reps = sets_reps[sets_start:sets_end]

            # Link sets to the current exercise
            for set_weight, set_reps in zip(exercise_sets_weight, exercise_sets_reps):
                set_entry = Set(reps=set_reps, weight=set_weight, exercise_id=exercise.id, user_id=current_user.id)
                db.session.add(set_entry)
                db.session.commit()

    return render_template("create_schedule.html")