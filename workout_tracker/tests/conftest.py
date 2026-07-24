import pytest
from workout_tracker import app as global_app_obj

@pytest.fixture()
def app():
    global_app_obj.config.update({
        "TESTING": True,
    })
    
    from workout_tracker.db import init_db
    from workout_tracker.db.seeder import seeder
    import workout_tracker.routes.auth
    import workout_tracker.routes.exercise
    import workout_tracker.routes.workout

    
    init_db()
    seeder()
    
    yield global_app_obj

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

