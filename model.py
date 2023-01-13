from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workouts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    duration = db.Column(db.Integer)
    date = db.Column(db.String(50))

    def __init__(self, type, duration, date):
        self.type = type
        self.duration = duration
        self.date = date
    def __repr__(self) :
        return "{} is the type and {} is the date".format(self.type,self.date)