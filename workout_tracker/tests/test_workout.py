import uuid


def test_create_workout(client):
    w1_name = f"{uuid.uuid4()}"
    w2_name = f"{uuid.uuid4()}"

    res = client.post('/workout', json={"exercises": [{"name":"push-up"},{"name":"squat", "sets":2, "reps":3},{"name":"plank"}], "workout_name":w1_name})
    assert res.status_code == 201
    res = client.post('/workout', json={"exercises": [{"name":"push-up"},{"name":"squat", "sets":2, "reps":3},{"name":"plank"}], "workout_name":w1_name})
    assert res.status_code == 409
    res = client.post('/workout', json={"exercises": [{"name":"push-"},{"name":"squat", "sets":2, "reps":3},{"name":"plank"}], "workout_name":w2_name})
    assert res.status_code == 404


def test_workout_ops(client):
    #### Creeate new workout plan ####

    res_c = client.post('/workout', json={"exercises": [{"name":"push-up"},{"name":"squat", "sets":2, "reps":3},{"name":"plank"}], "workout_name": f"{uuid.uuid4()}"})
    assert res_c.status_code == 201
    
    if res_c.json.get('data') is None:
        assert False

    workout_id = res_c.json['data']['workout_id']
    if workout_id is None:
        assert False
    
    #### Workout ops ####

    res_schd = client.put(f'/workout/{workout_id}/schedule', json={"date": '2026-07-30 01:00 EST'})
    assert res_schd.status_code == 200 
    
    res_start = client.put(f'/workout/{workout_id}/start')
    assert res_start.status_code == 200

    res_do = client.put(f'/workout/{workout_id}/do')
    assert res_do.status_code == 200

    res_delete = client.delete(f'workout/{workout_id}')
    assert res_delete.status_code == 204

def test_workout_exercises(client):
    #### Creeate new workout plan ####

    res_c = client.post('/workout', json={"exercises": [{"name":"push-up"},{"name":"squat", "sets":2, "reps":3},{"name":"plank"}], "workout_name": f"{uuid.uuid4()}"})
    assert res_c.status_code == 201
    
    if res_c.json.get('data') is None:
        assert False

    workout_id = res_c.json['data']['workout_id']
    if workout_id is None:
        assert False
   
    ### Due to database constraint, an exercise to be added to a workout plan, it has to exist in the exercises table.
    #### GET Exercises ####

    res_ex = client.get('/exercise') 
    assert res_ex.status_code == 200
    
    exercises = res_ex.json.get('exercises')
    if exercises is None:
        assert False

    #### get the first exercise name ####

    exercise_name = None
    for exe_name in exercises:
        exercise_name = exe_name
        break

    if exercise_name is None:
        assert False

    #### Workout exercise ops ####

    res_add_exercise = client.post(f'/workout/{workout_id}/exercise', json={"exercise": { "name":exercise_name, "sets":3, "reps":4, "weight":100 }}) 
    assert res_add_exercise.status_code == 200

    res_update_exercise = client.put(f'/workout/{workout_id}/exercise', json={"exercise": { "name":exercise_name, "sets":3, "reps":4, "weight":10 }}) 
    assert res_update_exercise.status_code == 200

    res_delete_exercise = client.delete(f'/workout/{workout_id}/exercise/{exercise_name}')
    assert res_delete_exercise.status_code == 204

def test_list_workouts(client):
    res = client.get('/workout')
    assert res.status_code == 200


