import psycopg2
from psycopg2.extras import execute_values

from workout_tracker import app
from workout_tracker.db import get_connection


user_data = [ ("Alice", "alice@gmail.com"), ("Bob", "bob@gmail.com"), ("Charlie", "charlie@gmail.com") ]
exercise_data = [("Push-up",), ("Squat",), ("Plank",), ("Burpee",)]

conn = get_connection()
cur = conn.cursor()

def seeder():
    try:
        cur.execute("SELECT COUNT(*) FROM users;")
        if cur.fetchone()[0] > 0:
            app.logger.info("Seeder skipped — data already exists.")
            return None

        execute_values(cur, 
                       "INSERT INTO users (name,email) VALUES %s RETURNING user_id",
                       user_data)
        user_ids = [row[0] for row in cur.fetchall()]

        execute_values(cur,
                       "INSERT INTO exercises (name) VALUES %s RETURNING exercise_id",
                       exercise_data)
        exercise_ids = [row[0] for row in cur.fetchall()]

        conn.commit()
        return {"user_ids": user_ids, "exercise_ids": exercise_ids}
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Failed seeding database {e}")
        return None
    finally:
        cur.close()
        conn.close()
