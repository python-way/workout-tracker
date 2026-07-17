from flask import Flask
app = Flask(__name__)

from workout_tracker.db import init_db
init_db()

from workout_tracker.db.seeder import seeder
seeder()

import workout_tracker.views
