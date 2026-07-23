import os
from dotenv import load_dotenv

from flask import Flask

app = Flask(__name__)

load_dotenv()

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

from workout_tracker.db import init_db
init_db()

from workout_tracker.db.seeder import seeder
seeder()

import workout_tracker.routes.auth
import workout_tracker.routes.workout
import workout_tracker.routes.exercise


