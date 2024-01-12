# Core imports
from fastapi import UploadFile
from sqlalchemy import select, and_, exc
from sqlalchemy.orm import joinedload
from core.db import session, standalone_session, Transactional
from core.utils import TokenHelper
from config import config

# App imports
from models import User, UserOtp, OtpType, File, Product
from errors import UserNotFound, UserDuplicate, OtpNotFound

from schemas import (
    CreateUserRequestSchema,
    UpdateUserRequestSchema,
    ChangePasswordRequestSchema,
    ChangeEmailRequestSchema,
    ChangePhoneRequestSchema,
    ForgotPasswordRequestSchema,

)
# Celery Tasks
from celery_task.tasks import send_mail_task

# Python imports
import hashlib
import uuid
from datetime import datetime, timedelta
import random
from typing import List


class UserServices:
    def __init__(self):
        ...

    """ Dynamic Query """
    async def get_user(self, user_id: int = None, email: str = None, phone: str = None, password: str = None) -> User:
        filters = set()

        if user_id:
            filters.add(User.id == user_id)
        if email:
            filters.add(User.email == email)
        if phone:
            filters.add(User.phone == phone)
        if password:
            hashed_pass = hashlib.md5(password.encode()).hexdigest()
            filters.add(User.password_hash == hashed_pass)

        query = (
            select(User)
            .options(joinedload(User.profile_image))
            .where(and_(*filters))
        )
        user = (await session.execute(query)).scalars().first()

        if not user:
            raise UserNotFound

        return user

    @standalone_session
    async def update_user(self, user_id: int, schema: UpdateUserRequestSchema) -> User:
        user: User = await self.get_user(user_id=user_id)
        for field, value in schema.model_dump().items():
            setattr(user, field, value)
        await session.commit()
        await session.refresh(user)
        return user

    @standalone_session
    async def update_user_avatar(self, user_id: int, file: File) -> User:
        user: User = await self.get_user(user_id=user_id)
        user.profile_image_id = file.id
        await session.commit()
        await session.refresh(user)
        return user

    @Transactional()
    async def delete_user(self, user_id: int) -> None:
        user: User = await self.get_user(user_id=user_id)
        session.delete(user)

    @Transactional()
    async def change_password(self, user_id: int, schema: ChangePasswordRequestSchema) -> None:
        user: User = await self.get_user(
            user_id=user_id, password=schema.old_password)
        hashed_pass = hashlib.md5(schema.new_password.encode()).hexdigest()
        user.password_hash = hashed_pass

    async def get_user_creation_token(self, schema: CreateUserRequestSchema) -> str:
        try:
            user = await self.get_user(email=schema.email)
            raise UserDuplicate
        except UserNotFound:
            payload = schema.model_dump()

            # Send otp to email with celery task
            def callback(otp_code: int, token: str):
                pass
                # send_mail_task.delay(schema.email, 'Otp Code', str(otp_code))

            return await self.__token_maker_for_verifier(payload, OtpType.register, callback=callback)

    async def get_change_mail_token(self, user_id: int, schema: ChangeEmailRequestSchema) -> str:
        try:
            email_is_exist = await self.get_user(email=schema.email)
            raise UserDuplicate
        except UserNotFound:
            user: User = await self.get_user(user_id=user_id)
            payload = {
                "user_id": user.id,
                "new_email": schema.email,
            }

            def callback(otp_code: str, token: str):
                # TODO: send otp_code to new mail (email)
                pass
            return await self.__token_maker_for_verifier(payload, OtpType.change_email, callback)

    async def get_change_phone_token(self, user_id: int, schema: ChangePhoneRequestSchema) -> str:
        try:
            phone_is_exist = await self.get_user(phone=schema.phone)
            raise UserDuplicate
        except UserNotFound:
            user: User = await self.get_user(user_id=user_id)
            payload = {
                "user_id": user.id,
                "phone": schema.phone,
            }

            def callback(otp_code: str, token: str):
                # TODO: send otp_code to new phone number
                pass
            return await self.__token_maker_for_verifier(payload, OtpType.change_phone, callback)

    async def get_reset_password_token(self, schema: ForgotPasswordRequestSchema) -> str:
        user: User = await self.get_user(email=schema.email)
        payload = {
            "user_id": user.id,
            "email": user.email,
        }

        def callback(otp_code: str, token: str):
            # TODO: send otp_code to user.email
            send_mail_task(email_address=user.email, subject='Şifre Sıfırlama',
                           content=f'exp://192.168.1.93:8081/--/ResetPassword?token={token}&otpCode={str(otp_code)}')
        return await self.__token_maker_for_verifier(payload, OtpType.reset_password, callback)

    async def __token_maker_for_verifier(self, payload: dict, otp_type: OtpType, callback: callable = None) -> str:
        """ 
        Helper Function :
        Generate a token for this functions:
        get_change_phone_token, get_change_mail_token, get_user_creation_token
        """
        minutes = config.OTP_CODE_EXPIRY_MINUTE
        otp: UserOtp = await self.generate_otp(otp_type)
        token_payload = payload.copy()
        token_payload["secret_key"] = otp.secret_key
        token_payload["is_authenticated"] = False
        token = TokenHelper.encode(
            payload=token_payload, expire_period=(minutes * 60))
        if callback is not None:
            callback(otp.otp_code, token)
        return token

    @standalone_session
    async def create_user(self, schema: CreateUserRequestSchema, profile_image_id: int = None) -> User:
        """ 
        Helper Function :
        Creating a user (with verification)
        """
        try:
            hashed_pass = hashlib.md5(schema.password.encode()).hexdigest()
            params = schema.model_dump()

            params["password_hash"] = hashed_pass
            del params["password"]

            user = User(**params,
                        profile_image_id=profile_image_id)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

        except exc.IntegrityError as e:
            raise UserDuplicate

    @standalone_session
    async def generate_otp(self, otp_type: OtpType, expiry_minutes: int = config.OTP_CODE_EXPIRY_MINUTE) -> UserOtp:
        """ 
        Helper Function :
        Generate Otp Code and write to db
        """
        if config.DEBUG == False:
            otp_code: int = random.randint(1000, 9999)
        otp_code: int = 1453

        secret_key = str(uuid.uuid4())
        now = datetime.now()
        expiry_date = now + timedelta(minutes=expiry_minutes)
        otp = UserOtp(
            secret_key=secret_key,
            # TODO maybe add token (for absolutely immutable any data)
            otp_code=otp_code,
            otp_type=otp_type,
            expiry_date=expiry_date,
            used=False
        )
        session.add(otp)
        await session.commit()
        await session.refresh(otp)
        return otp

    async def get_user_otp(self, otp_code: int, secret_key: str, otp_type: str) -> UserOtp:
        """ 
        Helper Function :
        Returning a OTP Model from matched secrets
        """
        now = datetime.now()
        otp: UserOtp = (await session.execute(
            select(UserOtp)
            .where(and_(
                UserOtp.otp_code == otp_code,
                UserOtp.expiry_date > now,
                UserOtp.secret_key == secret_key,
                UserOtp.used == False,
                UserOtp.otp_type == otp_type
            ))
        )).scalars().first()

        if not otp:
            raise OtpNotFound
        return otp

    @Transactional()
    async def consume_otp(self, otp: UserOtp):
        """ 
        Helper Function :
        Set Otp Code {used} parameter to "True"
        """
        otp.used = True
        return