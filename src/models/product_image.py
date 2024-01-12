from sqlalchemy import Column, Unicode, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import relationship
from core.db import Base
from core.db.mixins import Serializable


class ProductImage(Base, Serializable):
    __tablename__ = "product_images"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    image_id = Column(BigInteger, ForeignKey('files.id'), nullable=False)
    
