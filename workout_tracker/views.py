from workout_tracker import app
from workout_tracker.db.queries import ( 
         get_exercises,
         get_users,
         create_workout_with_exercises,
         update_workout_exercise,

         get_workouts,
         get_non_done_workouts,
         get_exercises_by_workout,
         schedule_workout,

         mark_workout_pending,
         mark_workout_done,
        )

from flask import request

current_user = '1'


# @app.route("/login", methods=["POST"])
# @app.route("/register", methods=["POST"])

@app.route("/workout", methods=["POST"])
def create_workout():
    data = request.get_json()
    if not data or 'exercises' not in data or 'workout_name' not in data:
        return {"message": f"Data provided is not complete"}, 400

    users = get_users()
    if not users or current_user not in users:
        return {"message": f"User not found"}, 404

    exercises = data.get('exercises')
    workout_name = data.get('workout_name')

    db_exercises = get_exercises()
    if not db_exercises:
        return {"message" : f"No exercieses found" }, 404

    for e in exercises:
        e_name = e.get("name")
        if not e_name:
            return {"message" : f"exercise name not found" }, 400

        if e_name.title() not in db_exercises.values():
            return { "message": f"Exercise {e_name} not found" }, 400

    success = create_workout_with_exercises(workout_name=workout_name,user_id=current_user, exercises=exercises)
   
    if not success:
        return {"message": f"Database transaction failed"}, 500

    return { "message": f"Workout created successfully" }, 201


@app.route("/workout/<workout_id>/schedule", methods=["PUT"])
def schd_workout(workout_id):
    data = request.get_json()
    
    if not data or 'date' not in data:
        return { "message" : "Data not found" }, 400
    
    workouts = get_workouts()

    if workout_id not in workouts:
        return { "message": "workout not found" }, 404

    success = schedule_workout(workout_id, data.get('date'))
    
    if not success:
        return {"message": f"Database transaction failed"}, 500

    return { "message": "workout scheduled successfully" }, 200


@app.route("/workout/<workout_id>/do", methods=["PUT"])
def do_workout(workout_id):
    workouts = get_workouts()

    if workout_id not in workouts:
        return { "message": "workout not found" }, 404

    success = mark_workout_done(workout_id)
 
    if not success:
        return {"message": f"Database transaction failed"}, 500

    return { "message" : "workout done successfully" } , 200

@app.route("/workout/<workout_id>/start", methods=["PUT"])
def start_workout(workout_id):
    workouts = get_workouts()

    if workout_id not in workouts:
        return { "message": "workout not found" }, 404

    success = mark_workout_pending(workout_id)
 
    if not success:
        return {"message": f"Database transaction failed"}, 500

    return { "message" : "workout started successfully" } , 200


@app.route("/workouts", methods=["GET"])
def active_workouts():
    workouts = get_non_done_workouts() 
    if not workouts:
        return { "message": "No workouts found" }, 200
    
    return {"workouts": workouts}, 200



@app.route("/workout/<workout_id>", methods=["PUT"])
def update_exercise(workout_id):
    data = request.get_json()
    if not data or 'exercise' not in data:
        return {"message": f"Data provided is not complete"}, 400

    users = get_users()
    if not users or current_user not in users:
        return {"message": f"User not found"}, 404

    exercise = data.get('exercise')

    db_exercises = get_exercises_by_workout(workout_id)
    if not db_exercises:
        return {"message" : f"No exercieses found" }, 404

    e_name = exercise.get("name")
    if not e_name:
        return {"message" : f"exercise name not found" }, 400

    for e in db_exercises:
        if e_name.title() in db_exercises.values():
            success = update_workout_exercise(workout_id=workout_id, exe=exercise)

            if not success:
                return {"message": f"Database transaction failed"}, 500

            return { "message": "Plan updated successfully" }, 200

    return { "message": f"Exercise {e_name} not found" }, 400

## DELETE exercise


## CASCADE Workout



# @app.route("/report", methods=["GET"])
# def generate_report():
#     workouts = get_done_workouts()
#     workouts = {f"workout[0]": workout[1] for workout in workouts}
#
#     if workout_id not in workouts:
#         return { "message": "workout not found" }
#
#     for each exercise
#     
#     workout_dict.exercise.type
#     workout_dict.exercise.sets
#     workout_dict.exercise.reps_number
#     workout_dict.exercise.weight
#     
