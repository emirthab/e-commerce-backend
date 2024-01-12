from pydantic import Field, BaseModel
from typing import Optional

from .file import FileSchema


class UserSchema(BaseModel):
    id: int = Field(...)
    email: str = Field(...)
    phone: Optional[str] = Field(None)
    full_name: str = Field(...)
    explanation: Optional[str] = Field(None)
    # TODO delete profile_image_id
    profile_image_path: Optional[str] = Field(None)

    class Config:
        from_attributes = True


class CreateUserRequestSchema(BaseModel):
    email: str = Field(...)
    full_name: str = Field(...)
    password: str = Field(...)


class TokenResponseSchema(BaseModel):
    token: str = Field(...)


class UpdateUserRequestSchema(BaseModel):
    full_name: Optional[str] = Field(None)
    explanation: Optional[str] = Field(None)


class UpdateUserAvatarResponseSchema(BaseModel):
    user_id: int = Field(None)
    profile_image_path: str = Field(None)


class ChangeEmailRequestSchema(BaseModel):
    email: str = Field(...)


class ChangePhoneRequestSchema(BaseModel):
    phone: str = Field(...)


class ChangePasswordRequestSchema(BaseModel):
    old_password: str = Field(...)
    new_password: str = Field(...)
