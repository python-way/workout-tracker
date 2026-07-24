from workout_tracker.db import get_connection
from psycopg2.extras import execute_values

from workout_tracker import app


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
            cur.execute("DELETE FROM workouts WHERE workout_id = %s", (workout_id,))
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

def update_workout_exe(workout_id, exe):
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


def list_non_done_workouts():
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

def get_workouts(filter_by=None, value=None):

    conn = get_connection()
    if filter_by:
        if value is None:
            raise ValueError("value should not be None")

        if filter_by.strip().lower() not in ['name', 'id']:
            raise Exception("filter_by not in ['name' or 'id']")
            return None
        
        #### Filter by name ####

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

        #### Filter by id ####

        elif filter_by == 'id':
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM workouts WHERE workout_id = %s", (value,))
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
    else:
        #### All workouts ####

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


def get_workout_exercises(workout_id, filter_by=None, value=None):
    conn = get_connection()
   
    if filter_by:
        if filter_by.strip().lower() not in ['exercise_name']:
            raise ValueError("filter_by is not valid. ['workout_id' or 'exercise_name']")

        if value is None:
            raise ValueError("value should be iterable not None")
            
        try:
            with conn.cursor() as cur:
               found_workout_exercises = []
               for exe in value:
                   cur.execute(" SELECT * FROM workout_exercises WHERE workout_id = %s AND exercise_name = %s ", (workout_id, exe.title()))
                   found_workout_exe = cur.fetchone()
                   if found_workout_exe is None:
                       return None
                   found_workout_exercises.append(found_workout_exe)

               return {f"{w_exe[0]}": {"exercise_name":w_exe[1], "sets":w_exe[2], "reps":w_exe[3], "weight":w_exe[4]}
                        for w_exe in found_workout_exercises}
        except Exception as e:
            conn.rollback()
            app.logger.error(f"Dataase error: {e}")
            return None
        finally:
            if conn:
                conn.close()

    else: 
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM workout_exercises WHERE workout_id = %s", (workout_id,))
                workout_exercises = cur.fetchall()

                return {f"{w_exe[0]}": {"exercise_name":w_exe[1], "sets":w_exe[2], "reps":w_exe[3], "weight":w_exe[4]}
                        for w_exe in workout_exercises}

        except Exception as e:
            conn.rollback()
            app.logger.error(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()

              
