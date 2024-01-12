from core.exceptions import CustomException

class UserDuplicate(CustomException):
    code = 400
    error_code = "USER_DUPLICATE"
    message = "duplicate email or phone"

class UserNotFound(CustomException):
    code = 404
    error_code = "USER_NOT_FOUND"
    message = "user not found"

class OtpNotFound(CustomException):
    code = 404
    error_code = "OTP_NOT_FOUND"
    message = "otp not found"

class UserDeviceNotFound(CustomException):
    code = 404
    error_code = "USER_DEVICE_NOT_FOUND"
    message = "user device or last token not found"