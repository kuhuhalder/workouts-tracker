from flask import jsonify, request
from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "workouts.db"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
app.app_context().push()
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

@app.route('/')
def hello_world(): 
 return render_template('index.html')
 
@app.route('/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == 'POST':
        data = request.get_json()
        workout = Workout(data['type'], data['duration'], data['date'])
        db.session.add(workout)
        db.session.commit()
        return jsonify({'success': True}), 201
    elif request.method == 'GET':
        workouts = Workout.query.all()
        return jsonify([workout.to_json() for workout in workouts])
    
@app.route('/workouts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def workout(id):
    workout = Workout.query.get(id)
    if request.method == 'PUT':
        data = request.get_json()
        workout.type = data['type']
        workout.duration = data['duration']
        workout.date = data['date']
        db.session.commit()
        return jsonify({'success': True}), 200
    elif request.method == 'DELETE':
        db.session.delete(workout)
        db.session.commit()
        return jsonify({'success': True}), 200
    elif request.method == 'GET':
        return jsonify(workout.to_json())
    
# Create a new workout
@app.route('/create_workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    workout = Workout(data['type'], data['duration'], data['date'])
    db.session.add(workout)
    db.session.commit()
    return jsonify({'success': True}), 201

# Retrieve all workouts
@app.route('/get_workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify([workout.to_json() for workout in workouts])

# Retrieve a specific workout
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    return jsonify(workout.to_json())

# Update a specific workout
@app.route('/workouts/<int:id>', methods=['PUT'])
def update_workout(id):
    workout = Workout.query.get(id)   
    data = request.get_json()
    workout.type = data['type']
    workout.duration = data['duration']
    workout.date = data['date']
    db.session.commit()
    return jsonify({'success': True}), 200

# Delete a specific workout
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({'success': True}), 200

if __name__ == '__main__':
    app.run(debug=True)