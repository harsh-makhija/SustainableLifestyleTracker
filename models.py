from datetime import datetime

import bcrypt

from app import app, db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, password, role, firstname, lastname):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.role = role
        self.registered_on = datetime.now()


class ExerciseLog(db.Model):
    __tablename__ = 'ExerciseLog'
    entry_num = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Integer, db.ForeignKey('users.email'))
    exercise_type = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    comments = db.Column(db.String(100), nullable=False)
    intensity = db.Column(db.String(100), nullable=False)

    def __init__(self, entry_num, email, exercise_type, duration, date, comments, intensity):
        self.entry_num = entry_num
        self.email = email
        self.exercise_type = exercise_type
        self.duration = duration
        self.date = date
        self.comments = comments
        self.intensity = intensity


class contact_form(db.Model):
    __tablename__ = 'ContactSubmissions'
    entry_num = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(100), nullable=False)

    def __init__(self, entry_num, message):
        self.entry_num = entry_num
        self.message = message


class Co2Values(db.Model):
    __tablename__ = 'CO2Values'
    id = db.Column(db.Float, primary_key=True)
    email = db.Column(db.String, db.ForeignKey('users.email'))
    transportval = db.Column(db.Float, nullable=True)
    foodval = db.Column(db.Float, nullable=True)
    electricalval = db.Column(db.Float, nullable=True)
    finalval = db.Column(db.Float, nullable=True)

    def __init__(self, id, transportval, foodval, electricalval, finalval, email):
        self.id = id
        self.email = email
        self.transportval = transportval
        self.foodval = foodval
        self.electricalval = electricalval
        self.finalval = finalval


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Creates test admin user
        admin = User(email='admin@email.com',
                     password='Admin1!',
                     firstname='Alice',
                     lastname='Jones',
                     role='admin')
        db.session.add(admin)
        db.session.commit()
