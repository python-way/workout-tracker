from workout_tracker.db import get_connection
from psycopg2.extras import execute_values

from workout_tracker import app


def get_exercises():
    conn = get_connection()

    try:
        with conn.cursor() as cur:
           cur.execute(" SELECT * FROM exercises; ")
           exercises = cur.fetchall()
           exercises = {f"{exercise[0]}":exercise[1] for exercise in exercises}
           return exercises
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Dataase error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_workouts():
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(" SELECT * FROM workouts; ")
            workouts = cur.fetchall()
            workouts = {f"{workout[0]}": workout[1] for workout in workouts}
            return workouts
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Dataase error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_non_done_workouts():
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(" SELECT * FROM workouts WHERE status <> 'done' ")
            workouts = cur.fetchall()
            workouts = {f"{workout[0]}": workout[1] for workout in workouts}
            return workouts
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

def create_workout_with_exercises(
        workout_name,
        user_id,
        exercises
        ):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute( "INSERT INTO workouts (workout_name, user_id, status) VALUES (%s,%s,%s) RETURNING  workout_id" ,
                         (workout_name, user_id, 'New')
                        )
            workout_id = cur.fetchone()[0]
            
            junctions = []
            for exe in exercises:
                junction = (workout_id,)
                exe_name = exe.get('name').title()
                exe_sets = exe.get('sets')
                exe_reps = exe.get('reps')
                exe_weight = exe.get('weight')

                junction += (exe_name, exe_sets, exe_reps, exe_weight)
                junctions.append(junction)
                
            execute_values( cur,
                            """INSERT INTO workout_exercises (workout_id, exercise_name, sets, reps, weight)
                               VALUES %s""",
                            junctions
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

def delete_workout_with_exercises(workout_id):
    conn = get_connection()

    try: 
        with conn.cursor() as cur:
            cur.execute("DELETE FROM workouts WHERE workout_id= %s", (workout_id,))
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()




def mark_workout_pending(workout_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE workouts SET status = %s WHERE workout_id = %s", ('pending', workout_id))
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()



def mark_workout_done(workout_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE workouts SET status = %s WHERE workout_id = %s", ('done', workout_id))
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()


def schedule_workout(workout_id, date):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE workouts SET schedule_time = %s WHERE workout_id = %s", (date, workout_id))
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        app.logger.error(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def update_workout_exercise(workout_id, exe):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE workout_exercises SET sets = %s, reps = %s, weight = %s WHERE workout_id = %s AND exercise_name = %s" ,                         
                        (exe.get('sets'), exe.get('reps'), exe.get('weight'), workout_id, exe.get('name').title())
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

def get_exercises_by_workout(workout_id):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM workout_exercises WHERE workout_id = %s", (workout_id,))
            exercises = cur.fetchall()
            exs = {f"{exercise[0]}":exercise[1] for exercise in exercises}
            exs_data = {f"{exercise[1]}": {"sets":exercise[2],"reps":exercise[3],"weight":exercise[4]} for exercise in exercises}

            conn.commit()
            return {"exercises":exs, "exercises_data":exs_data}

    except Exception as e:
        conn.rollback()
        app.logger.error(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()


def add_exercise_to_workout(workout_id, exe):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            exe_name = exe.get("name").title()
            sets = exe.get("sets")
            reps = exe.get("reps")
            weight = exe.get("weight")

            cur.execute("INSERT INTO workout_exercises (workout_id, exercise_name, sets, reps, weight) VALUES (%s,%s,%s,%s,%s)",
                        (workout_id, exe_name, sets, reps, weight)
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

def delete_workout_from_exercise(workout_id, exe_name):
    conn = get_connection()
    
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM workout_exercises WHERE (workout_id = %s AND exercise_name = %s)",
                        (workout_id, exe_name.title())
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



##### Exercises #####
def create_exe(exe):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO exercises (name, description, category, muscle) VALUES (%s,%s,%s,%s) ",
                        (exe.get("name").title(), exe.get("description"), exe.get("category"), exe.get("muscle"))
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

def update_exe(exe):
    conn = get_connection()
    
    try:
        with conn.cursor() as cur:
            exe_name = exe.get("name").title()
            exe_desc = exe.get("description")
            exe_cate = exe.get("category")
            exe_musc = exe.get("muscle")
            
            cur.execute("UPDATE exercises SET description = %s, category = %s, muscle = %s WHERE name = %s",
                        (exe_desc, exe_cate, exe_musc, exe_name)  
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

def delete_exe(exe_name):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM exercises WHERE name = %s", (exe_name,)) 
            conn.commit()
            return True

    except Exception as e:
        conn.rollback()
        app.logger.error(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()


