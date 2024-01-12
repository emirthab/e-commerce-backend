from sqlalchemy import Column, Unicode, BigInteger, Boolean
from sqlalchemy.ext.hybrid import hybrid_property

from config import config
from core.db import Base
from core.db.mixins import TimestampMixin, Serializable


class File(Base, TimestampMixin, Serializable):
    __tablename__ = "files"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    show_name = Column(Unicode(255), nullable=False)
    file_path = Column(Unicode(255), unique=True, nullable=False)
    extension = Column(Unicode(255), nullable=False)
    size = Column(Unicode(255), nullable=False)
    created_by = Column(BigInteger, nullable=True)

    @hybrid_property
    def download_url(self):
        return config.FIREBASE_STORAGE_URL + self.file_path