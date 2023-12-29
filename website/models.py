from . import db
from datetime import datetime
from sqlalchemy.sql import func
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    # Relationship with Schedule with back reference to user
    schedules = db.relationship("Schedule", backref="user", lazy=True)

class Schedule(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    exercises = db.relationship('Exercise', backref='schedule', lazy=True)

class Exercise(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String(100), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))

    sets = db.relationship('Set', backref='exercise', lazy=True)

class Set(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)