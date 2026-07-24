import os
from dotenv import load_dotenv

from flask import Flask

app = Flask(__name__)

load_dotenv()

# 1. Clear the compiled routing lookup tables
app.url_map._rules_by_endpoint.clear()

# 2. Clear the registered endpoints and paths
app.url_map._rules.clear()

# 3. Clear the registered view functions linked to those routes
app.view_functions.clear()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY environment variable must be set. "
        "Generate one with: python -c 'import secrets; print(secrets.token_hex(32))'"
    )

app.config["SECRET_KEY"] = SECRET_KEY

from workout_tracker.db import init_db
from workout_tracker.db.seeder import seeder

import workout_tracker.routes.auth
import workout_tracker.routes.workout
import workout_tracker.routes.exercise


if __name__ == "__main__":
    init_db()
    seeder()
