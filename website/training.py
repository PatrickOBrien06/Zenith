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

    return render_template("index.html", schedules=schedules, exercises=exercises, sets=sets, current_user=current_user, username=current_user.username)


# Create Schedule
@training.route("/schedule/create", methods=["POST", "GET"])
@login_required
def create_schedule():
    if request.method == "POST":
        schedule_name = request.form.get("schedule_name")
        exercise_names = request.form.getlist("exercise_name[]")
        
        if not schedule_name:
            # Check if schedule name is valid
            flash("Schedule name cannot be empty!", "danger")
            return render_template("create_schedule.html")

        exerciseCounter = 1

        # Check through exercise names to valid them
        for exercise_name in exercise_names:
            
            # If empty flash message and redirect user
            if exercise_name == "" or None:
                flash("Exercise name cannot be empty!", "danger")
                return render_template("create_schedule.html")

            sets_weight = request.form.getlist(f"set_weight_{exerciseCounter}[]")
            sets_reps = request.form.getlist(f"set_reps_{exerciseCounter}[]")

            # Check through sets weight and sets reps to valid
            for i, set_weight in enumerate(sets_weight):

                # If not numeric flash message and redirect user
                if not set_weight.isnumeric() or not sets_reps[i].isnumeric():
                    flash("Weight and reps must be a number!", "danger")
                    return render_template("create_schedule.html")
             
        # Save schudule
        schedule = Schedule(schedule_name=schedule_name, user_id=current_user.id)
        db.session.add(schedule)
        db.session.commit()

        # Loop for exercise_name to be used to grab all set data
        for exercise_name in exercise_names:

            sets_weight = request.form.getlist(f"set_weight_{exerciseCounter}[]")
            sets_reps = request.form.getlist(f"set_reps_{exerciseCounter}[]")

            exercise = Exercise(exercise_name=exercise_name, schedule_id=schedule.id, user_id=current_user.id)
            db.session.add(exercise)
            db.session.commit()

            exerciseCounter += 1

            # Loop through sets_weight, grabbing the value for each and grabbing the corrosponding set_reps
            for setCounter, i in enumerate(sets_weight):
                set_weight = sets_weight[setCounter]
                set_reps = sets_reps[setCounter]
                set = Set(reps=int(set_reps), weight=float(set_weight), exercise_id=exercise.id, user_id=current_user.id)
                db.session.add(set)
                db.session.commit()
            
        flash("Created schedule!", "success")
        return redirect(url_for("training.home", username=current_user.username))
    
    return render_template("create_schedule.html")


# Run Schedule
@training.route("/schedule/<schedule_id>", methods=["POST", "GET"])
@login_required
def run_schedule(schedule_id):
    schedule_name = Schedule.query.filter_by(id=schedule_id).first()
    exercises = Exercise.query.filter_by(schedule_id=schedule_id).all()
    sets = Set.query.filter_by(user_id=current_user.id).all()

    # Increased security not allowing the wrong user on an incorrect schedule
    if schedule_name.user_id != current_user.id:
        flash("You do not own that schedule!", "danger")
        return redirect(url_for("training.home", username=current_user.username))

    elif request.method == "POST":
        sets_id = request.form.getlist("id")

        # Check to see if all updated data is valid
        for set_id in sets_id:
            try:
                new_weight = int(request.form.get(f"new_weight_{set_id}"))
                new_reps = int(request.form.get(f"new_reps_{set_id}"))

            except ValueError: 
                flash("Weight and reps must be a number!", "danger")
                return render_template("run_schedule.html", schedule=schedule_name, exercises=exercises, sets=sets)

        # Loop to find each set's id
        for set_id in sets_id:
            
            new_weight = int(request.form.get(f"new_weight_{set_id}"))
            new_reps = int(request.form.get(f"new_reps_{set_id}"))

            # Update set data if new_weight and new_reps are numeric
            set = Set.query.filter_by(id=set_id).first()
            set.weight = new_weight
            set.reps = new_reps

            # Add set data to history
            set_record = History(reps=new_reps, weight=new_weight, set_id=set_id, user_id=current_user.id)
            db.session.add(set_record)
            db.session.commit()
        
        flash("Progress tracked!", "success")
        return redirect(url_for("training.home", username=current_user.username))
                    
    return render_template("run_schedule.html", schedule=schedule_name, exercises=exercises, sets=sets)