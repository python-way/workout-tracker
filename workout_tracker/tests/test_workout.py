import uuid

def test_create_workout(auth_client):
    w1_name = f"{uuid.uuid4()}"
    w2_name = f"{uuid.uuid4()}"

    payload = {"exercises": [{"name":"push-up"},{"name":"squat", "sets":2, "reps":3},{"name":"plank"}], "workout_name": w1_name}
    
    res = auth_client.post('/workout', json=payload)
    assert res.status_code == 201
    
    res = auth_client.post('/workout', json=payload)
    assert res.status_code == 409
    
    bad_payload = {"exercises": [{"name":"push-"},{"name":"squat", "sets":2, "reps":3},{"name":"plank"}], "workout_name": w2_name}
    res = auth_client.post('/workout', json=bad_payload)
    assert res.status_code == 404

def test_workout_ops(auth_client, workout_id):
    res_schd = auth_client.put(f'/workout/{workout_id}/schedule', json={"date": '2026-07-30 01:00 EST'})
    assert res_schd.status_code == 200 
    
    res_start = auth_client.put(f'/workout/{workout_id}/start')
    assert res_start.status_code == 200

    res_do = auth_client.put(f'/workout/{workout_id}/do')
    assert res_do.status_code == 200

    res_delete = auth_client.delete(f'workout/{workout_id}')
    assert res_delete.status_code == 204

def test_workout_exercises(auth_client, workout_id):
    res_ex = auth_client.get('/exercise')
    assert res_ex.status_code == 200
   
    exercises = res_ex.json.get('exercises')
    assert exercises is not None


    exercise_name = next(iter(exercises), None)
    assert exercise_name is not None

    res_add = auth_client.post(f'/workout/{workout_id}/exercise', json={"exercise": {"name": exercise_name, "sets": 3, "reps": 4, "weight": 100}}) 
    assert res_add.status_code == 200

    res_update = auth_client.put(f'/workout/{workout_id}/exercise', json={"exercise": {"name": exercise_name, "sets": 3, "reps": 4, "weight": 10}}) 
    assert res_update.status_code == 200

    res_delete = auth_client.delete(f'/workout/{workout_id}/exercise/{exercise_name}')
    assert res_delete.status_code == 204


def test_list_workouts(auth_client):
    res = auth_client.get('/workout')
    assert res.status_code == 200



