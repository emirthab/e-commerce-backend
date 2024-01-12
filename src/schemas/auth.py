from pydantic import BaseModel, Field
from .user import UserSchema


class LoginResponseSchema(BaseModel):
    token: str = Field(...)
    user: UserSchema = Field(...)


class LoginRequestSchema(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
    device_id: str = Field(...)


class VerifyOtpRequestSchema(BaseModel):
    token: str = Field(...)
    otp_code: int = Field(...)


class ForgotPasswordRequestSchema(BaseModel):
    email: str = Field(...)


class LoginOrRegisterWithFirebaseRequestSchema(BaseModel):
    id_token: str = Field(...)
    device_id: str = Field(...)
