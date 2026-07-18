from workout_tracker.db import get_connection
from psycopg2.extras import execute_values

from workout_tracker import app


def get_exercises():
    conn = get_connection()

    try:
        with conn.cursor() as cur:
           cur.execute(" SELECT * FROM exercises; ")
           exercises = cur.fetchall()
           return exercises
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Dataase error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_plans():
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(" SELECT * FROM plans; ")
            plans = cur.fetchall()
            return plans
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Dataase error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_users():
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(" SELECT * FROM users; ")
            users = cur.fetchall()
            return user
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Dataase error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def create_plan(plan_name, user_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO plans (plan_name, user_id) VALUES (%s, %s) RETURNING plan_id",
                (plan_name, user_id)
            )

            pid = cur.fetchone()[0]
            conn.commit()
            return pid

    except Exception as e:
        conn.rollback()
        app.logger.error(f"Dataase error: {e}")
        return None
    finally:
        if conn:
            conn.close()

## (plan_id, exercise_name)
def create_junctions(junctions):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            execute_values(
                        cur,
                        " INSERT INTO plan_exercises (plan_id, exercise_name) VALUES %s ",
                        junctions
                    )
            conn.commit()
            return len(junctions)

    except Exception as e:
        conn.rollback()
        app.logger.error(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()

