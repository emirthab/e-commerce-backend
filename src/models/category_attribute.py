from sqlalchemy import Column, Unicode, BigInteger, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base
from core.db.mixins import Serializable


class CategoryAttribute(Base, Serializable):
    __tablename__ = "category_attributes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    category_id = Column(BigInteger,ForeignKey('categories.id'), nullable=False)
    attribute_id = Column(BigInteger, ForeignKey('attributes.id'), nullable=False)
    
