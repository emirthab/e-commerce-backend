from sqlalchemy import Column, Unicode, BigInteger, Boolean, Text, DECIMAL, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from core.db import Base
from core.db.mixins import TimestampMixin, Serializable
import enum


class ProductOrderType(str, enum.Enum):
    suggested = 'suggested'
    price_desc = 'price_desc'  # Hight to low
    price_asc = 'price_asc'  # Low to high
    date_desc = 'date_desc'
    date_asc = 'date_asc'


class Product(Base, TimestampMixin, Serializable):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(Unicode(255), nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(BigInteger, nullable=False)
    price = Column(DECIMAL(12, 2), nullable=False)

    _images = relationship(
        "File",
        secondary='product_images',
        order_by='ProductImage.id.asc()',
        cascade="save-update, merge, delete",
    )
    attributes = relationship(
        "ProductAttribute",
        back_populates="product",
        cascade="save-update, merge, delete",
    )

    @hybrid_property
    def images(self):
        images = []
        for image in self._images:
            images.append({
                'id': image.id,
                'image_path': image.download_url
            })
        return images

    @hybrid_property
    def banner_image_path(self):
        return self._images[0].download_url if len(self._images) else None