import psycopg2
from psycopg2.extras import execute_values

from werkzeug.security import generate_password_hash, check_password_hash
from workout_tracker import app
from workout_tracker.db import get_connection


user_data = [ 
                 ("Alice", "alice@gmail.com", generate_password_hash("12345678")),
                 ("Bob", "bob@gmail.com", generate_password_hash("87654321")),
                 ("Charlie", "charlie@gmail.com", generate_password_hash("MyPassword")) 
             ]

exercise_data = [("Push-Up",), ("Squat",), ("Plank",), ("Burpee",)]

def seeder():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users;")
            if cur.fetchone()[0] > 0:
                app.logger.info("Seeder skipped — data already exists.")
                return None

            cur.execute("TRUNCATE TABLE exercises CASCADE")
            cur.execute("TRUNCATE TABLE workouts CASCADE")
            
            execute_values(cur, 
                           "INSERT INTO users (name,email,password) VALUES %s RETURNING user_id",
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
        conn.close()
