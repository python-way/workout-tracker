exercise_name = 'Exercise'

def test_create_exercise(client):
    res = client.post('/exercise', json={
            "name": exercise_name,
            "description": "My new exercise",
            "category": "upper body",
            "muscle": "trisips"
        })

    assert res.status_code == 201

def test_update_exercise(client):
    res = client.put('/exercise', json={
        "name": exercise_name,
            "description": "My new exercise",
            "category": "upper body",
            "muscle": "trisips"
        })

    assert res.status_code == 200

def test_delete_exercise(client):
    res = client.delete(f'/exercise/{exercise_name}')

    assert res.status_code == 204
