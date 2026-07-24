import uuid

w1_name = f"{uuid.uuid4()}"
w2_name = f"{uuid.uuid4()}"

def test_create_workout(client):
    res = client.post('/workout', json={"exercises": [{"name":"push-up"},{"name":"squat", "sets":2, "reps":3},{"name":"plank"}], "workout_name":w1_name})
    assert res.status_code == 201
    res = client.post('/workout', json={"exercises": [{"name":"push-up"},{"name":"squat", "sets":2, "reps":3},{"name":"plank"}], "workout_name":w1_name})
    assert res.status_code == 409
    res = client.post('/workout', json={"exercises": [{"name":"push-"},{"name":"squat", "sets":2, "reps":3},{"name":"plank"}], "workout_name":w2_name})
    assert res.status_code == 404

