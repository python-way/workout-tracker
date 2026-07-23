from flask import request

from werkzeug.security import generate_password_hash, check_password_hash
from workout_tracker.conf.auth import generate_token

from workout_tracker import app


from workout_tracker.db.queries.auth import ( 
         sign_up,
         get_user
        )

import workout_tracker.error.errors as error

############### Auth ############### 

@app.route("/register", methods=["POST"])
def register():
    """ Signing up a new user """
    data = request.get_json()
    if not data:
        return errors.NO_INPUT_400
   
    name, password, email = (
            data.get('name'),
            data.get('password'),
            data.get('email')
        )

    if name is None or password is None or email is None:
        return error.INVALID_INPUT_422

    name, password, email = name.strip(), password.strip(), email.strip() 
    
    user = get_user(filter_by="email", value=email)
    if user:
        return error.ALREADY_EXIST

    success = sign_up(name, email, generate_password_hash(password))

    if success is None:
        return error.FAILED_TRANSACTION_500

    return { "message": "User created successfully"}, 201

@app.route("/login", methods=["POST"])
def login():
    """ Signing in user """
    data = request.get_json()
    if not data:
        return error.NO_INPUT_400
    
    email, password = (
            data.get('email'),
            data.get('password')
    )

    if email is None or password is None:
        return error.INVALID_INPUT_422

    user = get_user(filter_by="email", value=email)
    if not user:
        return error.UNAUTHORIZED

    user_id, user_password = user.get("user_id"), user.get("password")
    if (user_id is None or user_password is None
        or not check_password_hash(user_password, password)
       ):
            return error.UNAUTHORIZED

    token = generate_token(user_id, minutes=30)

    return { "token": token }, 200
    
