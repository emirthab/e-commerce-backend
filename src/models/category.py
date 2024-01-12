from sqlalchemy import Column, Unicode, BigInteger, Boolean, Text, ForeignKey, select
from sqlalchemy.orm import relationship, column_property, relation
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from core.db import Base
from core.db.mixins import Serializable, NonRelationalOptions

from typing import List

class Category(Base, Serializable, NonRelationalOptions):
    __tablename__ = "categories"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    image_id = Column(BigInteger, ForeignKey('files.id'), nullable=True)
    parent_id = Column(BigInteger, ForeignKey('categories.id'), nullable=True)
    name = Column(Unicode(255), nullable=False)

    image = relationship('File', foreign_keys=[image_id], backref='categories')
    attributes = relationship('Attribute', secondary='category_attributes')

    sub_categories = relationship('Category', back_populates="parent_category")

    parent_category = relationship(
        'Category',
        remote_side=[id],          
        foreign_keys=[parent_id],  
    )