from core.exceptions import CustomException

class FileNotFoundException(CustomException):
    code = 404
    error_code = "FILE_NOT_FOUND"
    message = "file not found"
