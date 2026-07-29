import sys

from workout_tracker import app

from workout_tracker.db import init_db
from workout_tracker.db.seeder import seeder

if __name__ == "__main__":
    init_db()

    if "--seed" in sys.argv:
        seeder()

    app.run()

