from sqlalchemy import Column, Unicode, BigInteger, Boolean, Integer, DateTime, Enum

from core.db import Base
from core.db.mixins import TimestampMixin, Serializable
import enum


class OtpType(str, enum.Enum):
    register = 'register'
    reset_password = 'reset_password'
    change_email = 'change_email'
    change_phone = 'change_phone'


otp_types = [member.value for member in OtpType]


class UserOtp(Base, TimestampMixin, Serializable):
    __tablename__ = "user_otp"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    secret_key = Column(Unicode(255), nullable=False)
    otp_code = Column(Integer, nullable=False)
    # register || update_phone || update_mail
    otp_type = Column(Enum(*otp_types, create_constraint=True))
    expiry_date = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
