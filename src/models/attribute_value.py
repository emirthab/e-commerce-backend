from sqlalchemy import Column, Unicode, BigInteger, Boolean, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship, column_property, deferred

from core.db import Base
from core.db.mixins import Serializable


class AttributeValue(Base, Serializable):
    __tablename__ = "attribute_values"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    attribute_id = Column(BigInteger, ForeignKey('attributes.id'), nullable=False)
    name = Column(Unicode(255), nullable=False)
    attribute = relationship('Attribute', back_populates='values')
    

