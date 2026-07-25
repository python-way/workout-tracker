import sys
import pytest
from workout_tracker import app as global_app_obj
import uuid

@pytest.fixture()
def app():
    global_app_obj.config.update({
        "TESTING": True,
    })

    import workout_tracker.routes.auth
    import workout_tracker.routes.exercise
    import workout_tracker.routes.workout


    from workout_tracker.db import init_db
    from workout_tracker.db.seeder import seeder
    init_db()
    seeder()
    
    yield global_app_obj

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def auth_client(client):
    """Provides a client with a fresh, unique logged-in user session."""
    # user_id = uuid.uuid4()
    # email = f"{user_id}@gmail.com"
    # password = "12345678"
    #
    # client.post("/register", json={"name": str(user_id), "email": email, "password": password})
    # res_log = client.post("/login", json={"email": email, "password": password})
    #

    res_log = client.post("/login", json={"email": "admin@gmail.com", "password": "MyAdminPassword"})
    token = res_log.json['token']
    
    client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {token}"
    return client


@pytest.fixture()
def workout_id(auth_client):
    """Creates a fresh workout plan and returns its unique ID."""
    w_name = f"{uuid.uuid4()}"
    res = auth_client.post('/workout', json={
        "exercises": [{"name": "push-up"}, {"name": "squat", "sets": 2, "reps": 3}, {"name": "plank"}],
        "workout_name": w_name
    })
    return res.json['data']['workout_id']





