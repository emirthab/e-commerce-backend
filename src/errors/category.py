from core.exceptions import CustomException

class CategoryNotFound(CustomException):
    code = 404
    error_code = "CATEGORY_NOT_FOUND"
    message = "category not found"
