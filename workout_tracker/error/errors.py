SERVER_ERROR_500 = ({"message": "An error occured."}, 500)
FAILED_TRANSACTION_500 = ({"message": "Database transaction failed."}, 500)
NOT_FOUND_404 = ({"message": "Resource could not be found."}, 404)
NO_INPUT_400 = ({"message": "No input data provided."}, 400)
INVALID_INPUT_422 = ({"message": "Invalid input."}, 422)
ALREADY_EXIST = ({"message": "Already exists."}, 409)
UNAUTHORIZED = ({"message": "Wrong credentials."}, 401)

DOES_NOT_EXIST = ({"message": "Does not exists."}, 409)
