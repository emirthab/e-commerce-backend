from sqlalchemy import Column, Unicode, BigInteger, Boolean, ForeignKey, Enum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from config import config
from core.db import Base
from core.db.mixins import TimestampMixin, Serializable
import enum

class EventType(str, enum.Enum):
    favorite = "favorite"
    add_cart = "add_cart"
    purchase = "purchase"
    detail_open = "detail_open"
    
event_types = [member.value for member in EventType]

class Event(Base, TimestampMixin, Serializable):
    __tablename__ = "events"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    event_type = Column(Enum(*event_types, create_constraint=True), nullable=False)
    
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    user = relationship('User', foreign_keys=[user_id], backref="users")
    product = relationship('Product', foreign_keys=[product_id], backref="products")