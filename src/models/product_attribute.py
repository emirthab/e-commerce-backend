from sqlalchemy import Column, Unicode, BigInteger, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from core.db import Base
from core.db.mixins import Serializable


class ProductAttribute(Base, Serializable):
    __tablename__ = "product_attributes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    attribute_id = Column(BigInteger, ForeignKey('attributes.id'), nullable=False)
    attribute_value_id = Column(BigInteger, ForeignKey('attribute_values.id'), nullable=True)
    custom_attribute_value = Column(Unicode(255), nullable=True)
    
    product = relationship('Product', back_populates='attributes')
    attribute = relationship("Attribute", foreign_keys=[attribute_id], backref="product_attributes")
    attribute_value = relationship("AttributeValue", foreign_keys=[attribute_value_id], backref="product_attributes")

    @hybrid_property
    def name(self):
        return self.attribute.name
    
    @hybrid_property
    def value(self):
        if self.custom_attribute_value is not None:
            return self.custom_attribute_value
        elif self.attribute_value_id is not None:
            return self.attribute_value.name
        else:
            return None