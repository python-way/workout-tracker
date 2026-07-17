from workout_tracker import app
from workout_tracker.db 
import ( 
         get_connection,
         get_all_exercises,
         get_junction,

         create_plan,
         create_junction,

         delete_junction,

         user_found,
         
        )

current_user = 'alice@gmail.com'

@app.route("/plan", methods=["POST"])
def create_plan():
    data = request.get_json()
    if not data or 'exercises' not in data:
        return {"message": f"Data/Exercises not found"}, 400

    if not user_found(current_user):
        return {"message": f"User not found"}, 404

    exercises = data.get('exercises')
    all_exercises: list(tuple) = get_all_exercises()

    for e in exercises:
        if (e,) not in all_exercises:
            return { "message": f"Exercise {e} not found" }, 400

    plan: int = create_plan(current_user)

    junctions_to_create: list(tuple) = []
    for exercise in exercises:
        junctions_to_create.append(plan_id,exercise)
    create_junctions(junctions_to_create)

    return { "message": f"Plan created successfully" }, 201

@app.route("/plan", methods=["PUT"])
def update_plan():
    data = reqeust.get_json()
    if not data or 'exercises' not in data or 'plan_id' not in data:
        return {"message": f"Data not found"}, 400

    if not user_found(current_user):
        return {"message": f"User not found"}, 404
    
    exercises: list('str') = data.get('exercises')
    for e in exercises:
        if (e,) not in get_all_exercises():
            return { "message": f"Exercise {e} not found" }, 400

    junctions: list(tuple) = get_junctions(plan_id)
    _update_junctions(junctions, exercises, plan_id)

    return { "message": "Plan updated successfully" }, 200


def _update_junctions(junctions: list(tuple), exercises:list('str'), plan_id: int)
    same_junctions: list(tuple) = []

    for j in junctions:
        plan_id, exercise = j
        if exercise in exercises:
            exercises.remove(e)
            continue
        same_junctions.append(j)

    junctions_to_create: list(tuple) = []
    for exercise in exercises:
        junctions_to_create.append(plan_id,exercise)
    create_junctions(junctions_to_create)   

    delete_junctions(same_junctions)

