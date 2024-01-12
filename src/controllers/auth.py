# Core imports
from fastapi import APIRouter, Request
from fastapi.params import Param

# App imports
from schemas import (
    LoginResponseSchema,
    LoginRequestSchema,
    VerifyOtpRequestSchema,
    ForgotPasswordRequestSchema,
    LoginOrRegisterWithFirebaseRequestSchema
)

from services import AuthServices, UserServices
from models import OtpType
# Python imports
from typing import Optional

router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponseSchema,
)
async def login(schema: LoginRequestSchema):
    return await AuthServices().login(schema=schema)


@router.post(
    "/verify/{verification_type}",
)
async def otp_verify(schema: VerifyOtpRequestSchema, verification_type: OtpType, new_password: Optional[str] = Param(None, title="new_password", description="Fill in only when verification type is reset_password.")):
    await AuthServices().verify_otp(otp_type=verification_type, schema=schema, new_password=new_password)
    return 200


@router.post(
    "/forgot_password",
)
async def forgot_password(schema: ForgotPasswordRequestSchema):
    return await UserServices().get_reset_password_token(schema=schema)


@router.get(
    "/refresh_token",
    response_model=LoginResponseSchema,
)
async def refresh_token(token: str, device_id: str):
    return await AuthServices().refresh_token(token=token, device_id=device_id)


@router.delete(
    "/log_out",
)
async def log_out(device_id: str):
    await AuthServices().bulk_consume_devices(device_id=device_id)
    return 200
