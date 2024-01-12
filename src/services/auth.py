# Core imports
from sqlalchemy import select, and_, update, collate
from core.db import session, Transactional, standalone_session
from core.utils import TokenHelper
from core.fastapi.schemas.current_user import CurrentUser

# App imports
from .file import FileServices
from schemas import (
    LoginResponseSchema,
    LoginRequestSchema,
    VerifyOtpRequestSchema,
    CreateUserRequestSchema,
    LoginOrRegisterWithFirebaseRequestSchema,
    UserSchema,
)
from models import User, UserDevice, OtpType
from .user import UserServices
from errors import UserNotFound, Unauthorized, UserDeviceNotFound, FirebaseAuthError

# Python imports
from typing import Optional
import hashlib
from firebase_admin import auth
import random


class AuthServices:
    def __init__(self):
        ...

    async def get_auth_token(self, user: User) -> str:
        # The current_user value is for placing auth information,
        # ...authorization information in jwt.
        print(user.__dict__)
        current_user = CurrentUser(
            is_authenticated=True,
            role="user",
            **user.serialize()
        ).model_dump()
        token = TokenHelper.encode(payload=current_user)
        return token

    @Transactional()
    async def login(self, schema: LoginRequestSchema):
        try:
            user: User = await UserServices().get_user(email=schema.email, password=schema.password)
        except UserNotFound:
            raise Unauthorized

        await self.bulk_consume_devices(device_id=schema.device_id)

        token = await self.get_auth_token(user=user)
        user_device = UserDevice(
            user_id=user.id,
            device_id=schema.device_id,
            last_token=token,
            is_active=True
        )
        session.add(user_device)
        return LoginResponseSchema(token=token, user=user)

    @Transactional()
    async def refresh_token(self, token: str, device_id: str) -> LoginResponseSchema:
        user_device: UserDevice = await self.get_user_device(
            device_id=device_id,
            last_token=token
        )
        decoded_data = TokenHelper().decode_expired_token(token=token)
        if decoded_data["id"] is not user_device.user_id:
            raise Unauthorized
        user = await UserServices().get_user(user_id=user_device.user_id)
        token = await self.get_auth_token(user=user)
        user_device.last_token = token
        return LoginResponseSchema(token=token, user=user)

    @Transactional()
    async def verify_otp(self, otp_type: OtpType, schema: VerifyOtpRequestSchema, new_password: Optional[str] = None) -> None:
        decoded_result = TokenHelper.decode(token=schema.token)
        otp = await UserServices().get_user_otp(
            otp_code=schema.otp_code,
            secret_key=decoded_result["secret_key"],
            otp_type=otp_type
        )
        await UserServices().consume_otp(otp)

        match otp_type:
            case OtpType.register:
                create_user_schema = CreateUserRequestSchema(**decoded_result)
                await UserServices().create_user(schema=create_user_schema)
                return
            case OtpType.change_email:
                user: User = await UserServices().get_user(user_id=decoded_result["user_id"])
                user.email = decoded_result["new_email"]
            case OtpType.change_phone:
                user: User = await UserServices().get_user(user_id=decoded_result["user_id"])
                user.phone = decoded_result["phone"]
            case OtpType.reset_password:
                user: User = await UserServices().get_user(user_id=decoded_result["user_id"])
                hashed_pass = hashlib.md5(new_password.encode()).hexdigest()
                user.password_hash = hashed_pass


    async def get_user_device(self, device_id: str, last_token: str) -> UserDevice:
        """
        Helper Function :
        Returning a active UserDevice Model
        """
        user_device: UserDevice = (await session.execute(
            select(UserDevice)
            .where(and_(
                collate(UserDevice.device_id, "utf8_bin") == device_id,
                UserDevice.last_token == last_token,
                UserDevice.is_active == True
            ))
        )).scalars().first()

        if not user_device:
            raise UserDeviceNotFound

        return user_device

    @standalone_session
    async def bulk_consume_devices(self, device_id: str):
        """ 
        Helper Function :
        Bulk Updating devices (is_active=False)
        """
        await session.execute(
            update(UserDevice)
            .where(UserDevice.device_id == device_id)
            .values({
                "is_active": False
            })
        )
        await session.commit()
