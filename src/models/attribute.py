from sqlalchemy import Column, Unicode, BigInteger, Boolean, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import Serializable
import enum

class CustomInputType(str, enum.Enum):
    string = "string"
    integer = "integer"
    decimal = "decimal"
    
custom_input_types = [member.value for member in CustomInputType]

class Attribute(Base, Serializable):
    __tablename__ = "attributes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), nullable=False)
    is_required = Column(Boolean, nullable=False, default=False)
    show_in_filters = Column(Boolean, nullable=False, default=True)
    allow_multiple = Column(Boolean, nullable=False, default=False)
    allow_custom = Column(Boolean, nullable=False, default=False)
    custom_input_type = Column(Enum(*custom_input_types, create_constraint=True), nullable=True, default=None)
    input_prefix = Column(Unicode(255), nullable=True, default=None)
    
    values = relationship("AttributeValue", back_populates="attribute", cascade="all, delete-orphan")