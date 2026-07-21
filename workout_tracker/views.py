from flask import request

from werkzeug.security import generate_password_hash, check_password_hash

from workout_tracker import app
from workout_tracker.db.queries import ( 
         get_exercises,
         get_users,
         create_workout_with_exercises,
         delete_workout_with_exercises,

         add_exercise_to_workout,
         update_workout_exercise,
         delete_workout_from_exercise,
   
    
         #TODO:
         # create_exe,
         # update_exe,
         # delete_exe,
         # sign_up

         get_workouts,
         get_non_done_workouts,
         get_exercises_by_workout,
         schedule_workout,

         mark_workout_pending,
         mark_workout_done,
        )


current_user = '1'


### Auth

# @app.route("/login", methods=["POST"])
def register():
    """ Signing up a new user """
    data = request.get_json()
    
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')

    if not name or not password or not email:
        return {"message": "Name, email and password are required for registeration"}, 400

    users = get_users()
    if email in users.values():
        return {"message": f"Email {email} already exists" }, 400

    success = sign_up(name,generate_password_hash(password), email)
    if not success:
        return { "message": "Database transaction failed" }, 500

    return { "message": "User created successfully"}, 201

@app.route("/register", methods=["POST"])
def login():
    """ Signing in user """
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return {"message": "Email and password are required"}, 400

    users = get_users() 
    if email in users.values():
        return {"message": f"Email {email} already exists" }, 400
    
     
    user_password = get_user_password(email)
    if not password or not check_password_hash(user_password, password):
        return { "message": "Invalid credentials" }, 400
    
    jwt_data = {
                'id': user_id, 
                'exp': dt.datetime.utcnow() + dt.timedelta(minutes=30)
               }
            
    token = jwt.encode(
                jwt_data,
                app.config["SECRET_KEY"],
                algorithm="HS256"
            )

    return str(token)

############### Workout ###############

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
    if not data or 'exercises' not in data or 'workout_name' not in data:
        return {"message": "Data provided is not complete"}, 400

    users = get_users()
    if not users:
        return {"message": "Database query failed"}, 500

    if current_user not in users:
        return {"message": "User not found"}, 404

    exercises = data.get('exercises')
    workout_name = data.get('workout_name')

    db_exercises = get_exercises()
    if db_exercises is None:
        return {"message": "Database query failed"}, 500

    for e in exercises:
        e_name = e.get("name")
        if not e_name:
            return {"message" : "exercise name not found" }, 400

        if e_name.title() not in db_exercises.values():
            return { "message": f"Exercise {e_name} not found" }, 400

    success = create_workout_with_exercises(workout_name=workout_name,user_id=current_user, exercises=exercises)
   
    if not success:
        return {"message": "Database transaction failed"}, 500

    return { "message": "Workout created successfully" }, 201


@app.route("/workout/<workout_id>/schedule", methods=["PUT"])
def schd_workout(workout_id):
    """ 
        Scheduling a workout that's been created previously 

        Ex-Request Data: { 'date': '2026:07:21 01:00 EST' }
    """
    data = request.get_json()
    
    if not data or 'date' not in data:
        return { "message" : "Data not found" }, 400

    users = get_users()
    if not users:
        return {"message": "Database query failed"}, 500

    if current_user not in users:
        return {"message": "User not found"}, 404

    workouts = get_workouts()
    if workouts is None:
        return { "message": "Database query failed" }, 500

    if workout_id not in workouts:
        return { "message": "workout not found" }, 404

    success = schedule_workout(workout_id, data.get('date'))
    
    if not success:
        return {"message": "Database transaction failed"}, 500

    return { "message": "workout scheduled successfully" }, 200


@app.route("/workout/<workout_id>/start", methods=["PUT"])
def start_workout(workout_id):
    """ Marks workout as pending """
    workouts = get_workouts()
    if workouts is None:
        return { "message": "Database query failed" }, 500

    if workout_id not in workouts:
        return { "message": "workout not found" }, 404

    success = mark_workout_pending(workout_id)
 
    if not success:
        return {"message": "Database transaction failed"}, 500

    return { "message" : "workout started successfully" } , 200


@app.route("/workout/<workout_id>/do", methods=["PUT"])
def do_workout(workout_id):
    """ Marks workout as done """
    workouts = get_workouts()
    if workouts is None:
        return { "message": "Database query failed" }, 500

    if workout_id not in workouts:
        return { "message": "workout not found" }, 404

    success = mark_workout_done(workout_id)
 
    if not success:
        return {"message": "Database transaction failed"}, 500

    return { "message" : "workout done successfully" } , 200

@app.route("/workout/<workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    """ Deleting a workout """
    workouts = get_workouts()
    if workouts is None:
        return { "message": "Database query failed" }, 500

    if workout_id not in workouts:
        return { "message": "workout not found" }, 404

    success = delete_workout_with_exercises(workout_id=workout_id)
    if not success:
        return {"message": "Database transaction failed"}, 500

    return { "message" : "workout deleted successfully" }, 204

@app.route("/workout", methods=["GET"])
def list_workouts():
    """ List all non-done workouts """
    workouts = get_non_done_workouts() 
    if workouts is None:
        return { "message": "Database query failed" }, 500
    
    return {"workouts": workouts}, 200


############### Exercises  ###############

@app.route("/exercise", methods=["POST"])
def add_exercise():
    """ 
    Create an exercise
    
    Ex-Request Data: {"exercise": {"name":"Exercise", "description":"Details about the exercise", "category":"category", "muscle":"targeted muscle"}}
    """
    data = request.get_json()
    if not data or 'exercise' not in data:
        return {"message" : "Data not found" }, 400

    exercise = data.get("exercise")
    e_name = exercise.get("name")
    if not e_name:
        return {"message": "Exercise name is not found" }, 400

    db_exercises = get_exercises()
    if not db_exercises:
        return {"message": "Database query failed"}, 500
    
    if e_name.title() in db_exercises.values():
        return {"message": f"Exercise {e_name} already exists" }, 400

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
    if not data or 'exercise' not in data:
        return {"message" : "Data not found" }, 400

    exercise = data.get("exercise")
    e_name = exercise.get("name")
    if not e_name:
        return {"message": "Exercise name is not found" }, 400

    db_exercises = get_exercises()
    if not db_exercises:
        return {"message": "Database query failed"}, 500
    
    if e_name.title() not in db_exercises.values():
        return {"message": f"Exercise {e_name} does not exists" }, 400
    
    success = update_exe(exercise)
    if not success:
        return {"message": "Database transaction failed" }, 500

    return {"message" : "Exercise updated successfully"}, 200


@app.route("/exercise/<exercise_name>", methods=["DELETE"])
def delete_exercise():
    """ Delete an exercise """
 
    db_exercises = get_exercises()
    if not db_exercises:
        return {"message": "Database query failed"}, 500
    
    if exercise_name.title() not in db_exercises.values():
        return {"message": f"Exercise {e_name} does not exists" }
    
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

############### Workout's exercises ###############

@app.route("/workout/<workout_id>/exercise", methods=["POST"])
def add_workout_exercise(workout_id):
    """ 
    Adding an exercise to a workout

    Ex-Request Data: {"exercise": { "name":"Exercise", "sets":3, "reps":4, "weight":10 } }
    """
    data = request.get_json()
    if not data or 'exercise' not in data:
        return { "message" : "Data not found" }, 400
    
    # Exercise exist?
    exercise = data.get("exercise")
    e_name = exercise.get("name")
    if not e_name:
        return { "message" "Exercise name not found" }, 400

    db_exercises = get_exercises()
    if db_exercises is None:
        return {"message": "Database query failed"}, 500

    if e_name.title() not in db_exercises.values():
        return { "message": f"Exercise {e_name} not found" }, 400
        
    # Workout exist?
    workouts = get_workouts()
    if workouts is None:
        return { "message": "Database query failed" }, 500

    if workout_id not in workouts:
        return { "message": "workout not found" }, 404

    # Exercise alreayd exist in the workout plan?  
    db_query = get_exercises_by_workout(workout_id)
    if not db_query:
        return {"message": "Database query failed"}, 500

    db_workout_exercises = db_query.get("exercises")
    if not db_workout_exercises:
        return {"message" : "No exercieses found" }, 404

    if e_name.title() in db_workout_exercises.values():
        return { "message": f"Exercise {e_name} already exist" }, 400

    success = add_exercise_to_workout(workout_id=workout_id, exe=exercise)
    if not success:
        return {"message": "Database transaction failed"}, 500

    return { "message": "exercise added successfully" }, 200
 

@app.route("/workout/<workout_id>/exercise", methods=["PUT"])
def update_workout_exercise(workout_id):
    """
        Update workout's exercise 

        Ex-Request Data: { "exercise": {"name":"Exercise", "sets":3, "reps":3, "weight":5 }
    """ 
    data = request.get_json()
    if not data or 'exercise' not in data:
        return {"message": "Data provided is not complete"}, 400
    
    users = get_users()
    if not users:
        return {"message": "Database query failed"}, 500

    if current_user not in users:
        return {"message": "User not found"}, 404
    
    # Workout exist?
    workouts = get_workouts()
    if workouts is None:
        return { "message": "Database query failed" }, 500

    if workout_id not in workouts:
        return { "message": "workout not found" }, 404
    
    exercise = data.get('exercise')
    e_name = exercise.get("name")
    if not e_name:
        return {"message" : "exercise name not found" }, 400
    
    # Exercise exist in the workout plan?
    db_query = get_exercises_by_workout(workout_id)
    if not db_query:
        return {"message": "Database query failed"}, 500

    db_exercises = db_query.get("exercises")
    db_exercises_data = db_query.get("exercises_data")

    if not db_exercises or not db_exercises_data:
        return {"message" : "No exercieses found" }, 404

    if e_name.title() not in db_exercises.values():
        return { "message": f"Exercise {e_name} not found" }, 400
   
    exercise['sets'] = exercise.get("sets") if exercise.get("sets") else db_exercises_data.get(e_name.title()).get("sets")
    exercise['reps'] = exercise.get("reps") if exercise.get("reps") else db_exercises_data.get(e_name.title()).get("reps")
    exercise['weight'] = exercise.get("weight") if exercise.get("weight") else db_exercises_data.get(e_name.title()).get("weight")

    success = update_workout_exercise(workout_id=workout_id, exe=exercise)
    if not success:
        return {"message": "Database transaction failed"}, 500

    return { "message": "Plan updated successfully" }, 200

@app.route("/workout/<workout_id>/exercise/<exercise_name>", methods=["DELETE"])
def delete_workout_exercise(workout_id, exercise_name):
    """ Deleting workout's exercise """
    workouts = get_workouts()
    if workouts is None:
        return { "message": "Database query failed" }, 500

    if workout_id not in workouts:
        return { "message": "workout not found" }, 404
    
    # Exercise exist in the workout plan?
    db_query = get_exercises_by_workout(workout_id)
    if not db_query:
        return {"message": "Database query failed"}, 500

    db_exercises = db_query.get("exercises")
    if not db_exercises:
        return {"message" : "No exercieses found" }, 404

    if exercise_name.title() not in db_exercises.values():
        return { "message": f"Exercise {exercise_name} not found" }, 400

    success = delete_workout_from_exercise(workout_id=workout_id, exe_name=exercise_name)
    if not success:
        return {"message": "Database transaction failed"}, 500
    
    return {"message": "exercise deleted from workout successfully"}, 204


