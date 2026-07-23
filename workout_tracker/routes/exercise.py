from flask import request

from workout_tracker import app
import workout_tracker.error.errors as error

from workout_tracker.db.queries.exercise import (
         create_exe,
         update_exe,
         delete_exe,
         get_exercises,
    )

############### Exercises  ###############

@app.route("/exercise", methods=["POST"])
def add_exercise():
    """ 
    Create an exercise
    
    Ex-Request Data: {"name":"Exercise", "description":"Details about the exercise", "category":"category", "muscle":"targeted muscle"}
    """
    data = request.get_json()
    if not data:
        return error.NO_INPUT_400

    e_name = data.get("name")
    if not e_name:
        return error.INVALID_INPUT_422

    db_exercise = get_exercises(filter_by="name", value=[e_name])
    if db_exercise:
        return error.ALREADY_EXIST

    exercise = {"name":e_name, "description":data.get("description"), "category":data.get("category"), "muscle":data.get("muscle")}
    success = create_exe(exercise)
    if not success:
        return error.FAILED_TRANSACTION_500

    return {"message" : "Exercise created successfully"}, 201

@app.route("/exercise", methods=["PUT"])
def update_exercise():
    """ 
    Updates an exercise 

    Ex-Request Data: {"exercise": {"name":"Exercise", "description":"More details", "category":"another category", "muscle":"targeted muscle"}}
    """
    data = request.get_json()
    if not data:
        return error.NO_INPUT_400

    e_name = data.get("name")
    if not e_name:
        return error.INVALID_INPUT_422

    db_exercise = get_exercises(filter_by="name", value=[e_name])
    if db_exercise is None:
        return error.NOT_FOUND_404
    
    exercise = {"name":data.get("name"), "description":data.get("description"), "category":data.get("category"), "muscle":data.get("muscle")}
    success = update_exe(exercise)
    if not success:
        return error.FAILED_TRANSACTION_500

    return {"message" : "Exercise updated successfully"}, 200

@app.route("/exercise/<exercise_name>", methods=["DELETE"])
def delete_exercise(exercise_name):
    """ Delete an exercise """
    db_exercise = get_exercises(filter_by="name", value=[exercise_name])
    if db_exercise is None:
        return error.NOT_FOUND_404
    
    success = delete_exe(exercise_name)
    if not success:
        return error.FAILED_TRANSACTION_500
    
    return {"message" : "Exercise deleted successfully" }, 204

@app.route("/exercise", methods=["GET"])
def list_exercises():
    """ listing all exercises """
    db_exercises = get_exercises()
    if not db_exercises:
        return {"message": "Database query failed"}, 500
    
    return db_exercises , 200

