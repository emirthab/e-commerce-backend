from core.exceptions import CustomException


class Unauthorized(CustomException):
    code = 401
    error_code = "UNAUTHORIZED"
    message = "email or password is wrong"

class FirebaseAuthError(CustomException):
    code = 500
    error_code = "FIREBASE_AUTH_ERROR"
    message = "firebase auth error"