# Workout-Tracker
An API for a workout tracker application that allows users to manage their workouts and track their progress. 
It uses Flask with Authenticated routes (jwt) and postgres integration.
 
## Features
- 🔐 **Register / Login / Logout** with JSON requests
- 💪 **Workout Plan** - `create`, `update`, `delete`
- 🖲️ **Schedule / Start /  Do** workouts

## Tech stack

| Purpose          | Library                    |
| ---------------- | -------------------------- |
| Web framework    | Flask                      |
| Database         | postgres (psycopg2)        |
| Authentication   | pyjwt                      |
| Password hashing | Werkzeug                   |
| Tests            | pytest                     |

## Project structure

workout-tracker/
├── README.md
├── requirements.txt
├── .env
├── .gitignore
├── .git/
├── venv/
├── .pytest_cache/
└── workout_tracker/
    ├── __init__.py
    ├── conf/
    │   ├── __init__.py
    │   └── auth.py
    ├── db/
    │   ├── __init__.py
    │   ├── seeder.py       
    │   └── queries/
    │       ├── __init__.py
    │       ├── auth.py     
    │       ├── exercise.py
    │       └── workout.py
    ├── error/
    │   ├── __init__.py
    │   └── errors.py
    ├── routes/
    │   ├── auth.py
    │   ├── exercise.py
    │   └── workout.py
    └── tests/
        ├── __init__.py
        ├── conftest.py
        ├── test_auth.py
        ├── test_exercise.py
        └── test_workout.py

## Quick start
```bash
# 1. Get the code
git clone https://github.com/melihcolpan/flask-login-example
cd flask-login-example

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```
>> Note, Set .env with SECRET_KEY=YOUR_JWT_KEY, and your Postgres configrations

``` bash
# 4. Run it
flask --app workout_tracker run
```
The API is now running at **http://localhost:5000**.

## API Reference

### Base URL
`http://localhost:5000`

### Authentication
Most endpoints require a JWT token obtained from the `/login` endpoint. Include the token in the request header:
```
Authorization: Bearer <token>
```

---

## Authentication Routes

### 1. Register User
**POST** `/register`

Creates a new user account.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Success Response (201):**
```json
{
  "message": "User created successfully"
}
```

**Error Responses:**
- `400 Bad Request`: `{"message": "No input data provided."}`
- `422 Unprocessable Entity`: `{"message": "Invalid input."}`
- `409 Conflict`: `{"message": "Already exists."}` (email already registered)
- `500 Internal Server Error`: `{"message": "Database transaction failed."}`

---

### 2. Login User
**POST** `/login`

Authenticates a user and returns a JWT token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

**Success Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**
- `400 Bad Request`: `{"message": "No input data provided."}`
- `422 Unprocessable Entity`: `{"message": "Invalid input."}`
- `401 Unauthorized`: `{"message": "Wrong credentials."}`
- `500 Internal Server Error`: `{"message": "Database transaction failed."}`

---

## Exercise Routes

### 3. Create Exercise
**POST** `/exercise`

Creates a new exercise. (Admin operation)

**Request Body:**
```json
{
  "name": "Bench Press",
  "description": "Upper body pressing movement",
  "category": "Strength",
  "muscle": "Chest"
}
```

**Success Response (201):**
```json
{
  "message": "Exercise created successfully"
}
```

**Error Responses:**
- `400 Bad Request`: `{"message": "No input data provided."}`
- `422 Unprocessable Entity`: `{"message": "Invalid input."}`
- `409 Conflict`: `{"message": "Already exists."}`
- `500 Internal Server Error`: `{"message": "Database transaction failed."}`

---

### 4. Update Exercise
**PUT** `/exercise`

Updates an existing exercise. (Admin operation)

**Request Body:**
```json
{
  "name": "Bench Press",
  "description": "Updated description",
  "category": "Strength",
  "muscle": "Chest"
}
```

**Success Response (200):**
```json
{
  "message": "Exercise updated successfully"
}
```

**Error Responses:**
- `400 Bad Request`: `{"message": "No input data provided."}`
- `422 Unprocessable Entity`: `{"message": "Invalid input."}`
- `404 Not Found`: `{"message": "Resource could not be found."}`
- `500 Internal Server Error`: `{"message": "Database transaction failed."}`

---

### 5. Get All Exercises
**GET** `/exercise`

Lists all available exercises.

**Success Response (200):**
```json
{
  "exercises": [
    {
      "name": "Bench Press",
      "description": "Upper body pressing movement",
      "category": "Strength",
      "muscle": "Chest"
    },
    {
      "name": "Squats",
      "description": "Lower body compound movement",
      "category": "Strength",
      "muscle": "Legs"
    }
  ]
}
```

**Error Response:**
- `500 Internal Server Error`: `{"message": "Database query failed"}`

---

### 6. Delete Exercise
**DELETE** `/exercise/<exercise_name>`

Deletes an exercise. (Admin operation)

**URL Parameters:**
- `exercise_name` (string): Name of the exercise to delete

**Success Response (204):**
```json
{
  "message": "Exercise deleted successfully"
}
```

**Error Responses:**
- `404 Not Found`: `{"message": "Resource could not be found."}`
- `500 Internal Server Error`: `{"message": "Database transaction failed."}`

---

## Workout Routes

### 7. Create Workout
**POST** `/workout`

Creates a new workout plan with exercises. **Requires authentication.**

**Request Body:**
```json
{
  "workout_name": "Push Day",
  "exercises": [
    {
      "name": "Bench Press",
      "sets": 4,
      "reps": 8,
      "weight": 225
    },
    {
      "name": "Incline Dumbbell Press",
      "sets": 3,
      "reps": 10,
      "weight": 70
    }
  ]
}
```

**Success Response (201):**
```json
{
  "message": "Workout created successfully",
  "data": {
    "workout_id": 123
  }
}
```

**Error Responses:**
- `400 Bad Request`: `{"message": "No input data provided."}`
- `404 Not Found`: `{"message": "Resource could not be found."}`
- `409 Conflict`: `{"message": "Already exists."}`
- `422 Unprocessable Entity`: `{"message": "Invalid input."}`
- `500 Internal Server Error`: `{"message": "Database transaction failed."}`

---

### 8. List Workouts
**GET** `/workout`

Lists all active workouts for the authenticated user. **Requires authentication.**

**Success Response (200):**
```json
[
  {
    "workout_id": 1,
    "workout_name": "Push Day",
    "status": "scheduled",
    "date": "2026-07-25 10:00:00",
    "exercises": [
      {
        "name": "Bench Press",
        "sets": 4,
        "reps": 8,
        "weight": 225
      }
    ]
  }
]
```

**Error Response:**
- `500 Internal Server Error`: `{"message": "Database query failed"}`

---

### 9. Schedule Workout
**PUT** `/workout/<workout_id>/schedule`

Schedules a workout for a specific date. **Requires authentication.**

**URL Parameters:**
- `workout_id` (integer): ID of the workout

**Request Body:**
```json
{
  "date": "2026-07-25 10:00 EST"
}
```

**Success Response (200):**
```json
{
  "message": "Workout scheduled successfully"
}
```

**Error Responses:**
- `400 Bad Request`: `{"message": "No input data provided."}`
- `404 Not Found`: `{"message": "Resource could not be found."}`
- `422 Unprocessable Entity`: `{"message": "Invalid input."}`
- `500 Internal Server Error`: `{"message": "Database transaction failed."}`

---

### 10. Start Workout
**PUT** `/workout/<workout_id>/start`

Marks a workout as pending (started). **Requires authentication.**

**URL Parameters:**
- `workout_id` (integer): ID of the workout

**Success Response (200):**
```json
{
  "message": "Workout started successfully"
}
```

**Error Responses:**
- `404 Not Found`: `{"message": "Resource could not be found."}`
- `500 Internal Server Error`: `{"message": "Database transaction failed."}`

---

### 11. Complete Workout
**PUT** `/workout/<workout_id>/do`

Marks a workout as done/completed. **Requires authentication.**

**URL Parameters:**
- `workout_id` (integer): ID of the workout

**Success Response (200):**
```json
{
  "message": "Workout finished successfully"
}
```

**Error Responses:**
- `404 Not Found`: `{"message": "Resource could not be found."}`
- `500 Internal Server Error`: `{"message": "Database transaction failed."}`

---

### 12. Delete Workout
**DELETE** `/workout/<workout_id>`

Deletes a workout and all associated exercises. **Requires authentication.**

**URL Parameters:**
- `workout_id` (integer): ID of the workout to delete

**Success Response (204):**
```json
{
  "message": "Workout deleted successfully"
}
```

**Error Responses:**
- `404 Not Found`: `{"message": "Resource could not be found."}`
- `500 Internal Server Error`: `{"message": "Database transaction failed."}`

---

## Workout Exercise Routes

### 13. Add Exercise to Workout
**POST** `/workout/<workout_id>/exercise`

Adds an exercise to an existing workout. **Requires authentication.**

**URL Parameters:**
- `workout_id` (integer): ID of the workout

**Request Body:**
```json
{
  "exercise": {
    "name": "Dumbbell Flyes",
    "sets": 3,
    "reps": 12,
    "weight": 50
  }
}
```

**Success Response (200):**
```json
{
  "message": "Exercise added successfully"
}
```

**Error Responses:**
- `400 Bad Request`: `{"message": "No input data provided."}`
- `404 Not Found`: `{"message": "Resource could not be found."}`
- `409 Conflict`: `{"message": "Already exists."}`
- `422 Unprocessable Entity`: `{"message": "Invalid input."}`
- `500 Internal Server Error`: `{"message": "Database transaction failed."}`

---

### 14. Update Workout Exercise
**PUT** `/workout/<workout_id>/exercise`

Updates an exercise within a workout (sets, reps, weight). **Requires authentication.**

**URL Parameters:**
- `workout_id` (integer): ID of the workout

**Request Body:**
```json
{
  "exercise": {
    "name": "Bench Press",
    "sets": 5,
    "reps": 5,
    "weight": 245
  }
}
```

**Success Response (200):**
```json
{
  "message": "Workout updated successfully"
}
```

**Error Responses:**
- `400 Bad Request`: `{"message": "No input data provided."}`
- `404 Not Found`: `{"message": "Resource could not be found."}`
- `422 Unprocessable Entity`: `{"message": "Invalid input."}`
- `500 Internal Server Error`: `{"message": "Database transaction failed."}`

---

### 15. Delete Exercise from Workout
**DELETE** `/workout/<workout_id>/exercise/<exercise_name>`

Removes an exercise from a workout. **Requires authentication.**

**URL Parameters:**
- `workout_id` (integer): ID of the workout
- `exercise_name` (string): Name of the exercise to remove

**Success Response (204):**
```json
{
  "message": "Exercise deleted from workout successfully"
}
```

**Error Responses:**
- `404 Not Found`: `{"message": "Resource could not be found."}`
- `500 Internal Server Error`: `{"message": "Database transaction failed."}`

---

## Error Response Codes

| Code | Error                  | Message                                |
| ---- | ---------------------- | -------------------------------------- |
| 400  | Bad Request            | `No input data provided.`              |
| 401  | Unauthorized           | `Wrong credentials.`                   |
| 404  | Not Found              | `Resource could not be found.`         |
| 409  | Conflict               | `Already exists.`                      |
| 422  | Unprocessable Entity   | `Invalid input.`                       |
| 500  | Internal Server Error  | `Database transaction failed.`         |

---

## Usage Example

```bash
# 1. Register
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword"
  }'

# 2. Login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword"
  }'
# Returns: {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}

# 3. Create a workout (use token from login)
curl -X POST http://localhost:5000/workout \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "workout_name": "Push Day",
    "exercises": [
      {
        "name": "Bench Press",
        "sets": 4,
        "reps": 8,
        "weight": 225
      }
    ]
  }'
```

## Running the tests
``` bash
pytest
```

## Inspiration
https://roadmap.sh/projects/fitness-workout-tracker
