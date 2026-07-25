import uuid

exercise_name = f"{uuid.uuid4()}"

def test_create_exercise(auth_client):
    res = auth_client.post('/exercise', json={
            "name": exercise_name,
            "description": "My new exercise",
            "category": "upper body",
            "muscle": "trisips"
        })

    assert res.status_code == 201

def test_update_exercise(auth_client):
    res = auth_client.put('/exercise', json={
        "name": exercise_name,
            "description": "My new exercise",
            "category": "upper body",
            "muscle": "trisips"
        })

    assert res.status_code == 200

def test_delete_exercise(auth_client):
    res = auth_client.delete(f'/exercise/{exercise_name}')
    assert res.status_code == 204

def test_list_exercise(auth_client):
    res = auth_client.get('/exercise')
    assert res.status_code == 200
