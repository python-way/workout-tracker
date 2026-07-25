from flask import request

from workout_tracker import app
import workout_tracker.error.errors as error

from workout_tracker.db.queries.exercise import (
         create_exe,
         update_exe,
         delete_exe,
         get_exercises,
    )
from workout_tracker.conf.auth import token_required

############### Exercises  ###############

@app.route("/exercise", methods=["POST"])
@token_required
def add_exercise(current_user):
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

    try:
        db_exercise = get_exercises(filter_by="name", value=[e_name], user_id=current_user)
        if db_exercise:
            return error.ALREADY_EXIST
    except PermissionError as e:
        app.logger.error("Permission error")
        return error.UNAUTHORIZED


    exercise = {"name":e_name, "description":data.get("description"), "category":data.get("category"), "muscle":data.get("muscle")}
    success = create_exe(exercise)
    if not success:
        return error.FAILED_TRANSACTION_500

    return {"message" : "Exercise created successfully"}, 201

@app.route("/exercise", methods=["PUT"])
@token_required
def update_exercise(current_user):
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
    
    try:
        db_exercise = get_exercises(filter_by="name", value=[e_name], user_id=current_user)
        if db_exercise is None:
            return error.NOT_FOUND_404
    except PermissionError as e:
        app.logger.error("Permission error")
        return error.UNAUTHORIZED

  
    exercise = {"name":data.get("name"), "description":data.get("description"), "category":data.get("category"), "muscle":data.get("muscle")}
    success = update_exe(exercise)
    if not success:
        return error.FAILED_TRANSACTION_500

    return {"message" : "Exercise updated successfully"}, 200

@app.route("/exercise/<exercise_name>", methods=["DELETE"])
@token_required
def delete_exercise(current_user, exercise_name):
    """ Delete an exercise """

    try:
        db_exercise = get_exercises(filter_by="name", value=[exercise_name], user_id=current_user)
        if db_exercise is None:
            return error.NOT_FOUND_404
    except PermissionError as e:
        app.logger.error("Permission error")
        return error.UNAUTHORIZED

    success = delete_exe(exercise_name)
    if not success:
        return error.FAILED_TRANSACTION_500
    
    return {"message" : "Exercise deleted successfully" }, 204

@app.route("/exercise", methods=["GET"])
@token_required
def list_exercises(current_user):
    """ listing all exercises """
    try:
        db_exercises = get_exercises(current_user)
        if not db_exercises:
            return {"message": "Database query failed"}, 500
    except PermissionError as e:
        app.logger.error("Permission error")
        return error.UNAUTHORIZED

    return { "exercises": db_exercises } , 200 

