from workout_tracker.db import get_connection
from psycopg2.extras import execute_values

from workout_tracker import app


def sign_up(name, email, password):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
                         (name, email, password)
                        )

            conn.commit()
            return True

    except Exception as e:
        conn.rollback()
        app.logger.error(f"Database error: {e}")
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
            us = {f"{user[2]}": str(user[0]) for user in users}
            us_data = {f"{user[0]}": {"name": user[1], "email": user[2], "password": user[3] } for user in users}

            return {"users":us, "users_data": us_data}
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Dataase error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_user(filter_by, value):
    conn = get_connection()

    if filter_by.strip().lower() not in ['email', 'user_id']:
        raise Exception("filter_by not in ['email' or 'user_id']")
        return None

    if filter_by == 'email':
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE email = %s", (value,))
                user = cur.fetchone()
                if user:
                    return {"user_id":user[0], "username":user[1], "email":user[2], "password":user[3]}
                return None

        except Exception as e:
            conn.rollback()
            app.logger.error(f"Dataase error: {e}")
            return None
        finally:
            if conn:
                conn.close()

    if filter_by == 'user_id':
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE user_id = %s", (value,))
                user = cur.fetchone()
                if user:
                    return {"user_id":user[0], "username":user[1], "email":user[2], "password":user[3]}
                return None

        except Exception as e:
            conn.rollback()
            app.logger.error(f"Dataase error: {e}")
            return None
        finally:
            if conn:
                conn.close()
