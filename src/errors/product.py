from core.exceptions import CustomException

class ProductNotFound(CustomException):
    code = 404
    error_code = "PRODUCT_NOT_FOUND"
    message = "product not found"

class AttributeRequired(CustomException):
    code = 400
    error_code = "ATTRIBUTE_REQUIRED"
    message = "an attribute required for a product in this category was not submitted"
