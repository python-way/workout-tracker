from workout_tracker import app
from workout_tracker.db.queries import ( 
         get_exercises,
         # create_workout
        )

from flask import request

current_user = 'alice@gmail.com'


# @app.route("/login", methods=["POST"])
# @app.route("/register", methods=["POST"])

@app.route("/workout", methods=["POST"])
def add_workout():
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

    db_exercises_dict = {f"{exercise[0]}":exercise[1] for exercise in db_exercises}

    for e in exercises:
        e_name = e.get("name")
        if not e_name:
            return {"message" : f"exercise name not found" }, 400

        if e_name.title() not in db_exercises_dict.values():
            return { "message": f"Exercise {e_name} not found" }, 400

    # per each exercise
    # sets = exercise.sets
    # reps = exercise.reps
    # weight = exercise.weight
   
    success = create_workout_with_exercises(user_id=1,workout_name=workout_name, exercises=exercises)

    success = True
    if not success:
        return {"message": f"Database transaction failed"}, 500

    return { "message": f"Plan created successfully" }, 201

# @app.route("/workout", methods=["PUT"])
# def update_workout():
#     data = reqeust.get_json()
#     if not data or 'exercises' not in data or 'workout_id' not in data:
#         return {"message": f"Data not found"}, 400
#
#     users = get_users()
#     if not users or current_user not in users:
#         return {"message": f"User not found"}, 404
#
#     exercises = data.get('exercises')
#     db_exercises = get_exercises()
#
#     for e_name in exercises:
#         if e_name.title() not in exercises_dict.values():
#             return { "message": f"Exercise {e_name} not found" }, 400
#     
#     success = update_workout_with_exercises(workout_id=workout_id, exercises=exercises)
#
#     if not success:
#         return {"message": f"Database transaction failed"}, 500
#
#     return { "message": "Plan updated successfully" }, 200
#
# @app.route("/workout/<workout_id>", methods=["DELETE"])
# def delete_workout(workout_id):
#
#     users = get_users()
#     if not users or current_user not in users:
#         return {"message": f"User not found"}, 404
#     
#     success = delete_plan_with_exercises(plan_id=plan_id)
#
#     if not success:
#         return {"message": f"Database transaction failed"}, 500
#
#     return { "message": "Plan deleted successfully" }, 204
#
# @app.route("/workout/<workout_id>/schedule", methods=["POST"])
# def schedule_workout(workout_id):
#     data = request.get_json()
#
#     if not data or 'days' not in data or 'times' not in data:
#         return { "message" : "Data not found" }
#
#     success = schedule_workout(workout_id, data['days'], data['times'])
#     
#     if not success:
#         return {"message": f"Database transaction failed"}, 500
#
#     return { "message": "workout scheduled successfully" }, 200
#
# @app.route("/workouts", methods=["GET"])
# def active_workouts():
#     workouts = get_workouts() 
#     if not workouts:
#         return { "message": "No workouts found" }, 200
#     return {"workouts": workouts}, 200
#
# @app.route("/workout/<workout_id>", methods=["POST"])
# def do_workout(workout_id):
#     workouts = get_workouts()
#     workouts_dict = {f"workout[0]": workout[1] for workout in workouts}
#
#     if workout_id not in workouts_dict:
#         return { "message": "workout not found" }
#
#     success = mark_workout_done(workout_id)
#  
#     if not success:
#         return {"message": f"Database transaction failed"}, 500
#
#     return { "message" : "workout done successfully" } , 200
#
#
# @app.route("/workout/<workout_id>", methods=["POST"])
# def start_workout(workout_id):
#     workouts = get_workouts()
#     workouts_dict = {f"workout[0]": workout[1] for workout in workouts}
#
#     if workout_id not in workouts_dict:
#         return { "message": "workout not found" }
#
#     success = mark_workout_pending(workout_id)
#  
#     if not success:
#         return {"message": f"Database transaction failed"}, 500
#
#     return { "message" : "workout started successfully" } , 200
#
# @app.route("/report", methods=["GET"])
# def generate_report():
#     workouts = get_done_workouts()
#     workouts_dict = {f"workout[0]": workout[1] for workout in workouts}
#
#     if workout_id not in workouts_dict:
#         return { "message": "workout not found" }
#
#     for each exercise
#     
#     workout_dict.exercise.type
#     workout_dict.exercise.sets
#     workout_dict.exercise.reps_number
#     workout_dict.exercise.weight
#     
