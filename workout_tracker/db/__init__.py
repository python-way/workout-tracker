import os

import psycopg2
from psycopg2 import sql, OperationalError, errors

from workout_tracker import app

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "workout"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except OperationalError as oe:
        app.logger.error(f"Database connection failed: {oe}")
        return None

def init_db():
    conn = get_connection()
    if conn:
        try: 
            with conn.cursor() as cur:
                cur.execute("""CREATE TABLE IF NOT EXISTS exercises (
                                exercise_id bigserial,
                                name varchar(50) UNIQUE,
                                description varchar(250),
                                category varchar(50),
                                muscle varchar(50),
                                CONSTRAINT exercise_key PRIMARY KEY (exercise_id)
                                );
                            """)

                cur.execute("""CREATE TABLE IF NOT EXISTS users (
                                user_id bigserial,
                                name varchar(50),
                                email varchar(255),
                                CONSTRAINT user_key PRIMARY KEY (user_id),
                                CONSTRAINT user_email_unique UNIQUE (name, email));
                            """)
                cur.execute("""CREATE TABLE IF NOT EXISTS plans (
                                plan_id bigserial,
                                plan_name varchar(50) UNIQUE,
                                user_id integer REFERENCES users (user_id),
                                CONSTRAINT plan_key PRIMARY KEY (plan_id)
                            );""")

                cur.execute("""CREATE TABLE IF NOT EXISTS plan_exercises (
                                plan_id integer REFERENCES plans (plan_id),
                                exercise_name varchar(100) REFERENCES exercises (name),
                                CONSTRAINT plan_exercise_key PRIMARY KEY (plan_id, exercise_name)
                            );""")
                conn.commit()
        except Exception as e:
            app.logger.error(f"Error initializing DB: {e}")
        finally:
            conn.close()
