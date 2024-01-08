from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for
from .models import User, Schedule, Exercise, Set, History 
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


# Run Schedule
@training.route("/run_schedule/<schedule_id>", methods=["POST", "GET"])
@login_required
def run_schedule(schedule_id):
    schedule_name = Schedule.query.filter_by(id=schedule_id).first()
    exercises = Exercise.query.filter_by(user_id=current_user.id, schedule_id=schedule_id).all()
    sets = Set.query.filter_by(user_id=current_user.id).all()

    if request.method == "POST":
        ex_id = request.form.getlist("ex_id")
        new_weight = request.form.getlist("new_weight")
        new_reps = request.form.getlist("new_reps")
        sets_id = request.form.getlist("id")

        for set_id in sets_id:
            for setCounter in range(len(new_weight)):

                # Update set data
                weight = float(new_weight[setCounter])
                reps = int(new_reps[setCounter])
                set = Set.query.filter_by(id=set_id).first()
                set.weight = weight
                set.reps = reps
                db.session.commit()

                # Add set data to history
            set_record = History(reps=reps, weight=weight, set_id=set_id, user_id=current_user.id)
            db.session.add(set_record)
            db.session.commit()

            print(set_record.set_id)
            
        records = History.query.all()

        for record in records:
                print(record.id)
                    
    return render_template("run_schedule.html", schedule=schedule_name, exercises=exercises, sets=sets)

