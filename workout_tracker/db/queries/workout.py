from workout_tracker.db import get_connection
from psycopg2.extras import execute_values

from workout_tracker import app


def create_workout_with_exercises(
        workout_name,
        workout_id,
        exercises
        ):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute( "INSERT INTO workouts (workout_name, workout_id, status) VALUES (%s,%s,%s) RETURNING  workout_id" ,
                         (workout_name, workout_id, 'New')
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

def delete_exercise_from_workout(workout_id, exe_name):
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

def get_workout(filter_by, value):

    conn = get_connection()

    if filter_by.strip().lower() not in ['name', 'id']:
        raise Exception("filter_by not in ['name' or 'id']")
        return None

    if filter_by == 'name':
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM workouts WHERE workout_name = %s", (value,))
                workout = cur.fetchone()
                if workout:
                    return {"id":workout[0], "workout_name":workout[1], "user_id":workout[2], "status":workout[3], "schedule_time": workout[4]}
                return None

        except Exception as e:
            conn.rollback()
            app.logger.error(f"Dataase error: {e}")
            return None
        finally:
            if conn:
                conn.close()

