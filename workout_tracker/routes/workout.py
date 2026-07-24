from flask import request

from workout_tracker import app

import workout_tracker.error.errors as error

from workout_tracker.db.queries.auth import get_users
from workout_tracker.db.queries.exercise import get_exercises
from workout_tracker.db.queries.workout import (
         create_workout_with_exercises,
         delete_workout_with_exercises,

         add_exercise_to_workout,
         update_workout_exe,
         delete_exercise_from_workout,

         get_workouts,
         get_workout_exercises,
         list_non_done_workouts,
         schedule_workout,
         mark_workout_pending,
         mark_workout_done,

       )

from workout_tracker.conf.auth import token_required

current_user = 1

############## Workout ###############

@app.route("/workout", methods=["POST"])
def create_workout():
    """
    Creating workout plan with exercises
    
    Ex-Request data: { "workout_name": "MyFirstPlan", 
                        "exercises": [
                                      {"name": "Exercise1", "sets":3, "reps":4, "weight":10},
                                      ...
                                     ]
                     }
    """
    data = request.get_json()
    if not data:
        return error.NO_INPUT_400

    exercises = data.get('exercises')
    workout_name = data.get('workout_name')
    
    if exercises is None or workout_name is None:
        return error.INVALID_INPUT_422

    user = get_users(filter_by='user_id', value=current_user)
    if not user:
        return error.UNAUTHORIZED
    
    workout = get_workouts(filter_by="name", value=workout_name)
    if workout:
        return error.ALREADY_EXIST

    valid_exercises_names = [exe.get('name') for exe in exercises]
    if None in valid_exercises_names:
        return error.INVALID_INPUT_404

    db_exercises = get_exercises(filter_by="name", value=valid_exercises_names) 
    if db_exercises is None:
        return error.NOT_FOUND_404
    
    success = create_workout_with_exercises(workout_name, current_user, exercises)

    if not success:
        return error.FAILED_TRANSACTION_500

    return { "message": "Workout created successfully" }, 201


@app.route("/workout/<workout_id>/schedule", methods=["PUT"])
def schd_workout(workout_id):
    """ 
        Scheduling a workout that's been created previously 

        Ex-Request Data: { 'date': '2026:07:21 01:00 EST' }
    """
    data = request.get_json()
    if not data:
        return error.NO_INPUT_400
    
    date = data.get("date")
    if date is None:
        return error.INVALID_INPUT_422

    workout = get_workouts(filter_by="id", value=workout_id)
    if workout is None:
        return error.NOT_FOUND_404

    success = schedule_workout(workout_id, date)
    
    if not success:
        return error.FAILED_TRANSACTION_500

    return { "message": "Workout scheduled successfully" }, 200


@app.route("/workout/<workout_id>/start", methods=["PUT"])
def start_workout(workout_id):
    """ Marks workout as pending """
    workout = get_workouts(filter_by="id", value=workout_id)
    if workout is None:
        return error.NOT_FOUND_404

    success = mark_workout_pending(workout_id)
    if not success:
        return error.FAILED_TRANSACTION_500

    return { "message" : "Workout started successfully" } , 200


@app.route("/workout/<workout_id>/do", methods=["PUT"])
def do_workout(workout_id):
    """ Marks workout as done """
    workout = get_workouts(filter_by="id", value=workout_id)
    if workout is None:
        return error.NOT_FOUND_404

    success = mark_workout_done(workout_id)
    if not success:
        return error.FAILED_TRANSACTION_500

    return { "message" : "Workout finished successfully" } , 200

@app.route("/workout/<workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    """ Deleting a workout """
    workout = get_workouts(filter_by="id", value=workout_id)
    if workout is None:
        return error.NOT_FOUND_404

    success = delete_workout_with_exercises(workout_id)
    if not success:
        return error.FAILED_TRANSACTION_500

    return { "message" : "Workout deleted successfully" }, 204

@app.route("/workout", methods=["GET"])
def list_workouts():
    """ List all non-done workouts """
    workouts = list_non_done_workouts() 
    if workouts is None:
        return { "message": "Database query failed" }, 500
    
    return workouts, 200


############### Workout's exercises ###############

@app.route("/workout/<workout_id>/exercise", methods=["POST"])
def add_workout_exercise(workout_id):
    """ 
    Adding an exercise to a workout

    Ex-Request Data: {"exercise": { "name":"Exercise", "sets":3, "reps":4, "weight":10 } }
    """
    data = request.get_json()
    if not data:
        return error.NO_INPUT_400

    exercise = data.get("exercise")
    if exercise is None:
        return error.INVALID_INPUT_422

    e_name = exercise.get("name")
    if e_name is None:
        return error.INVALID_INPUT_422

    db_exercise = get_exercises(filter_by="name", value=[e_name])
    if db_exercise is None:
        return error.NOT_FOUND_404
        
    workout = get_workouts(filter_by="id", value=workout_id)
    if workout is None:
        return error.NOT_FOUND_404

    db_workout_exercise = get_workout_exercises(workout_id, filter_by="exercise_name", value=[e_name])
    if db_workout_exercise:
        return error.ALREADY_EXIST

    success = add_exercise_to_workout(workout_id=workout_id, exe=exercise)
    if not success:
        return error.FAILED_TRANSACTION_500

    return { "message": "Exercise added successfully" }, 200
 

@app.route("/workout/<workout_id>/exercise", methods=["PUT"])
def update_workout_exercise(workout_id):
    """
        Update workout's exercise 

        Ex-Request Data: { "exercise": {"name":"Exercise", "sets":3, "reps":3, "weight":5 }
    """ 
    data = request.get_json()
    if not data:
        return error.NO_INPUT_400

    exercise = data.get("exercise")
    if exercise is None:
        return error.INVALID_INPUT_422

    e_name = exercise.get("name")
    if e_name is None:
        return error.INVALID_INPUT_422
          
    workout = get_workouts(filter_by="id", value=workout_id)
    if workout is None:
        return error.NOT_FOUND_404

    db_workout_exercise = get_workout_exercises(workout_id, filter_by="exercise_name", value=[e_name])
    if db_workout_exercise is None:
        return error.NOT_FOUND_404

    sets = exercise.get('sets')
    reps = exercise.get('reps')
    weight = exercise.get('weight')

    if sets is None:
        exercise["sets"] = db_workout_exercise.get(workout_id).get('sets')
    if reps is None:
        exercise["reps"] = db_workout_exercise.get(workout_id).get('reps')
    if weight is None:
        exercise["weight"] = db_workout_exercise.get(workout_id).get('weight')
    

    success = update_workout_exe(workout_id, exercise)
    if not success:
        return error.FAILED_TRANSACTION_500

    return { "message": "Workout updated successfully" }, 200



@app.route("/workout/<workout_id>/exercise/<exercise_name>", methods=["DELETE"])
def delete_workout_exercise(workout_id, exercise_name):
    """ Deleting workout's exercise """
    workout = get_workouts(filter_by="id", value=workout_id)
    if workout is None:
        return error.NOT_FOUND_404

    db_workout_exercise = get_workout_exercises(workout_id, filter_by="exercise_name", value=[exercise_name])
    if db_workout_exercise is None:
        return error.NOT_FOUND_404

    success = delete_exercise_from_workout(workout_id, exercise_name)
    if not success:
        return error.FAILED_TRANSACTION_500
    
    return {"message": "Exercise deleted from workout successfully"}, 204
