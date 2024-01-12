from sqlalchemy import Column, Unicode, BigInteger, Boolean, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from core.db import Base
from core.db.mixins import TimestampMixin, Serializable

from config import config

class User(Base, TimestampMixin, Serializable):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(Unicode(255), nullable=False, unique=True)
    phone = Column(Unicode(255), nullable=True, unique=True)
    password_hash = Column(Unicode(255), nullable=False, unique=False)
    full_name = Column(Unicode(255), nullable=False, unique=False)
    profile_image_id = Column(BigInteger, ForeignKey('files.id'), nullable=True, unique=False)
    profile_image = relationship("File", foreign_keys=[profile_image_id], backref="users")
    explanation = Column(Text, nullable=True, unique=False)

    @hybrid_property
    def profile_image_path(self):
        return config.FIREBASE_STORAGE_URL + self.profile_image.file_path