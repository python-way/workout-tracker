import os
from dotenv import load_dotenv

from flask import Flask

app = Flask(__name__)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY environment variable must be set. "
        "Generate one with: python -c 'import secrets; print(secrets.token_hex(32))'"
    )

app.config["SECRET_KEY"] = SECRET_KEY

from workout_tracker.db import init_db
init_db()

from workout_tracker.db.seeder import seeder
seeder()

import workout_tracker.routes.auth
import workout_tracker.routes.workout
import workout_tracker.routes.exercise


