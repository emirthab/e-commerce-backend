# Core imports
from fastapi import APIRouter, Request, Depends, UploadFile
from core.exceptions import ForbiddenException
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAuthenticated,
)
# App imports
from schemas import (
    UserSchema,
    CreateUserRequestSchema,
    TokenResponseSchema,
    UpdateUserRequestSchema,
    ChangeEmailRequestSchema,
    ChangePasswordRequestSchema,
    ChangePhoneRequestSchema,
    UpdateUserAvatarResponseSchema,
    ProductSchema
)

from services import UserServices, FileServices

# Python imports
from typing import List

router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=UserSchema,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_user(request: Request, user_id: int):
    user = await UserServices().get_user(user_id=user_id)
    return user


@router.post(
    "",
    response_model=TokenResponseSchema,
)
async def create_user(schema: CreateUserRequestSchema):
    token = await UserServices().get_user_creation_token(schema=schema)
    return TokenResponseSchema(token=token)


@router.put(
    "/{user_id}",
    response_model=UserSchema,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def update_user(request: Request, user_id: int, schema: UpdateUserRequestSchema):
    # Access control
    if request.user.id is not user_id:
        raise ForbiddenException
    return await UserServices().update_user(user_id=user_id, schema=schema)


@router.patch(
    "/{user_id}/email",
    response_model=TokenResponseSchema,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def change_email(request: Request, user_id: int, schema: ChangeEmailRequestSchema):
    # Access control
    if request.user.id is not user_id:
        raise ForbiddenException
    token = await UserServices().get_change_mail_token(user_id=user_id, schema=schema)
    return TokenResponseSchema(token=token)


@router.patch(
    "/{user_id}/password",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def change_password(request: Request, user_id: int, schema: ChangePasswordRequestSchema):
    # Access control
    if request.user.id is not user_id:
        raise ForbiddenException
    return await UserServices().change_password(user_id=user_id, schema=schema)


@router.patch(
    "/{user_id}/phone",
    response_model=TokenResponseSchema,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def change_phone(request: Request, user_id: int, schema: ChangePhoneRequestSchema):
    # Access control
    if request.user.id is not user_id:
        raise ForbiddenException
    token = await UserServices().get_change_phone_token(user_id=user_id, schema=schema)
    return TokenResponseSchema(token=token)


@router.patch(
    "/{user_id}/avatar",
    response_model=UpdateUserAvatarResponseSchema,
    # dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def change_user_avatar(request: Request, user_id: int, file: UploadFile):
    # # Access control
    # if request.user.id is not user_id:
    #     raise ForbiddenException
    uploaded_file = await FileServices().upload(file=file, user_id=user_id)
    user = await UserServices().update_user_avatar(user_id=user_id, file=uploaded_file)
    return UpdateUserAvatarResponseSchema(
        user_id=user.id,
        profile_image_path=user.profile_image_path
    )


@router.delete(
    "/{user_id}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
async def delete_user(request: Request, user_id: int):
    # Access control
    if request.user.id is not user_id:
        raise ForbiddenException
    return await UserServices().delete_user(user_id=user_id)