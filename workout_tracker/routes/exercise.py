from flask import request

from workout_tracker import app
from workout_tracker.error import errors

from workout_tracker.db.queries.exercise import (
         create_exe,
         update_exe,
         get_exercises,
         delete_exe,
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
        return {"message" : "Data not found"}, 400

    e_name = data.get("name")
    if not e_name:
        return {"message": "Exercise name is not found" }, 400

    db_exercises = get_exercises()
    if not db_exercises:
        return {"message": "Database query failed"}, 500
    
    if e_name.title() in db_exercises.values():
        return {"message": f"Exercise {e_name} already exists" }, 400

    exercise = {"name":data.get("name"), "description":data.get("description"), "category":data.get("category"), "muscle":data.get("muscle")}
    success = create_exe(exercise)
    if not success:
        return {"message": "Database transaction failed" }, 500

    return {"message" : "Exercise created successfully"}, 201

@app.route("/exercise", methods=["PUT"])
def update_exercise():
    """ 
    Updates an exercise 

    Ex-Request Data: {"exercise": {"name":"Exercise", "description":"More details", "category":"another category", "muscle":"targeted muscle"}}
    """
    data = request.get_json()
    if not data:
        return {"message" : "Data not found"}, 400

    e_name = data.get("name")
    if not e_name:
        return {"message": "Exercise name is not found" }, 400

    db_exercises = get_exercises()
    if not db_exercises:
        return {"message": "Database query failed"}, 500
    
    if e_name.title() not in db_exercises.values():
        return {"message": f"Exercise {e_name} does not exists" }, 400
    
    exercise = {"name":data.get("name"), "description":data.get("description"), "category":data.get("category"), "muscle":data.get("muscle")}
    success = update_exe(exercise)
    if not success:
        return {"message": "Database transaction failed" }, 500

    return {"message" : "Exercise updated successfully"}, 200


@app.route("/exercise/<exercise_name>", methods=["DELETE"])
def delete_exercise(exercise_name):
    """ Delete an exercise """
 
    db_exercises = get_exercises()
    if not db_exercises:
        return {"message": "Database query failed"}, 500
    
    if exercise_name.title() not in db_exercises.values():
        return {"message": f"Exercise {exercise_name} does not exists" }
    
    success = delete_exe(exercise_name)
    if not success:
        return {"message": "Database transaction failed" }, 500
    
    return {"message" : "Exercise deleted successfully" }, 204
   

@app.route("/exercise", methods=["GET"])
def list_exercises():
    """ listing all exercises """
    db_exercises = get_exercises()
    if not db_exercises:
        return {"message": "Database query failed"}, 500
    
    return { "Exercises": db_exercises }, 200

