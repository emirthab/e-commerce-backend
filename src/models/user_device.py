from sqlalchemy import Column, Unicode, BigInteger, Boolean, Text

from core.db import Base
from core.db.mixins import TimestampMixin, Serializable


class UserDevice(Base, TimestampMixin, Serializable):
    __tablename__ = "user_devices"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, unique=False)
    device_id = Column(Unicode(255), nullable=False, unique=False)
    last_token = Column(Text, nullable=False, unique=False)
    is_active = Column(Boolean, nullable=False, default=True)
