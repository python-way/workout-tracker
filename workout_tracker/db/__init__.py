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
                                password varchar(255),
                                CONSTRAINT user_key PRIMARY KEY (user_id),
                                CONSTRAINT user_email_unique UNIQUE (name, email));
                            """)
                cur.execute("""CREATE TABLE IF NOT EXISTS workouts (
                                workout_id bigserial,
                                workout_name varchar(50),
                                user_id integer REFERENCES users (user_id),
                                status varchar(50),
                                schedule_time timestamp with time zone,
                                CONSTRAINT workout_key PRIMARY KEY (workout_id),
                                CONSTRAINT workout_name_user UNIQUE (workout_name, user_id)
                            );""")

                cur.execute("""CREATE TABLE IF NOT EXISTS workout_exercises (
                                workout_id integer REFERENCES workouts (workout_id) ON DELETE CASCADE,
                                exercise_name varchar(100) REFERENCES exercises (name) ON DELETE CASCADE,
                                sets integer NULL,
                                reps integer NULL,
                                weight real NULL,

                                CONSTRAINT workout_exercise_key PRIMARY KEY (workout_id, exercise_name)
                            );""")
                conn.commit()
        except Exception as e:
            app.logger.error(f"Error initializing DB: {e}")
        finally:
            conn.close()
