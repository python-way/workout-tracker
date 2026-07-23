from workout_tracker.db import get_connection
from psycopg2.extras import execute_values

from workout_tracker import app

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
            cur.execute("DELETE FROM exercises WHERE name = %s", (exe_name.title(),)) 
            conn.commit()
            return True

    except Exception as e:
        conn.rollback()
        app.logger.error(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()


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

def get_exercises(filter_by, value):
    conn = get_connection()
    
    if filter_by.strip().lower() == "name":
        
        try:
            with conn.cursor() as cur:
               found_exercises = []
               for exe in value:
                   cur.execute(" SELECT * FROM exercises WHERE name = %s ", (exe.title(),))
                   found_exe = cur.fetchone()
                   if found_exe is None:
                       return None
                   found_exercises.append(found_exe)

               return {f"{exe[1]}": {"id":exe[0], "description":exe[1], "category":exe[2], "muscle":exe[3]}
                        for exe in found_exercises}
               return True
        except Exception as e:
            conn.rollback()
            app.logger.error(f"Dataase error: {e}")
            return None
        finally:
            if conn:
                conn.close()

