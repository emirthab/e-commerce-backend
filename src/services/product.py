# Core imports
from core.db import standalone_session, session, Transactional
from sqlalchemy import select, update, delete, insert, and_, func, desc, or_
from sqlalchemy.orm import joinedload

# App imports
from models import Product, ProductImage, ProductAttribute, AttributeValue, ProductOrderType
from schemas import (
    CreateProductRequestSchema,
    UpdateProductRequestSchema
)
from errors import ProductNotFound

# Python imports
from typing import List, Dict, Union
import re
import operator

class ProductServices:
    def __init__(self) -> None:
        ...

    async def get_products_with_filter(self, page: int, per_page: int, category_id: int, search: str, order_by: ProductOrderType, attributes: Dict[str, Union[str, int]]) -> tuple[int, List[Product]]:
        filters = [Product.category_id == category_id]

        if search:
            filters.append(Product.title.like(f'%{search}%'))

        for key, value in attributes.items():
            attr_id = re.search(r'a_(\d+)', key).group(1)
            if key.endswith(('_min', '_max')):
                comparison_op = operator.lt if key.endswith('_max') else operator.gt
                filters.append(Product.attributes.any(
                    and_(ProductAttribute.attribute_id == attr_id, comparison_op(ProductAttribute.custom_attribute_value, value))
                ))
            elif isinstance(value, list):
                or_filters = [ProductAttribute.attribute_value_id == val for val in value]
                filters.append(Product.attributes.any(
                    and_(ProductAttribute.attribute_id == attr_id, or_(*or_filters))
                ))
            else:
                filters.append(Product.attributes.any(
                    and_(ProductAttribute.attribute_id == attr_id, ProductAttribute.attribute_value_id == value)
                ))

        order_mapping = {
            ProductOrderType.suggested: Product.id,
            ProductOrderType.price_asc: Product.price,
            ProductOrderType.price_desc: desc(Product.price),
            ProductOrderType.date_asc: Product.updated_at,
            ProductOrderType.date_desc: desc(Product.updated_at),
        }
        order = order_mapping.get(order_by, Product.id)

        total_items_count_query = select(func.count(Product.id).over()).where(and_(*filters))

        query = (
            select(Product)
            .options(joinedload(Product._images))
            .options(joinedload(Product.attributes))
            .where(and_(*filters))
            .order_by(order)
            .limit(per_page)
            .offset(page * per_page)
        )

        products = (await session.execute(query)).scalars().unique().all()
        total_items = (await session.execute(total_items_count_query)).scalar() or 0

        return total_items, products

    async def get_product_detail_by_id(self, product_id) -> Product:
        query = (
            select(Product)
            .options(joinedload(Product._images))
            .options(joinedload(Product.attributes).joinedload(ProductAttribute.attribute_value))
            .options(joinedload(Product.attributes).joinedload(ProductAttribute.attribute))
            .where(Product.id == product_id))
        product: Product = (await session.execute(query)).scalars().first()
        if not product:
            raise ProductNotFound

        return product
    
    async def get_all_product_details(self) -> List[Product]:
        query = (
            select(Product)
            .options(joinedload(Product._images))
            .options(joinedload(Product.attributes).joinedload(ProductAttribute.attribute_value))
            .options(joinedload(Product.attributes).joinedload(ProductAttribute.attribute))
            )
        products : List[Product] = (await session.execute(query)).scalars().unique().all()

        return products

    @standalone_session
    async def create_product(self, category_id: int, schema: CreateProductRequestSchema) -> Product:
        product = Product(
            title=schema.title,
            description=schema.description,
            price=schema.price,
            category_id=category_id,
        )
        session.add(product)
        await session.commit()
        await session.refresh(product)

        # Images
        images = [
            ProductImage(
                product_id=product.id,
                image_id=image_id,
            )
            for image_id in schema.images
        ]
        session.add_all(images)

        # Attributes
        attributes = [
            ProductAttribute(
                product_id=product.id,
                attribute_id=attribute.attribute_id,
                attribute_value_id=attribute.attribute_value_id if hasattr(
                    attribute, 'attribute_value_id') else None,
                custom_attribute_value=attribute.custom_value if hasattr(
                    attribute, 'custom_value') else None,
            )
            for attribute in schema.attributes
        ]
        session.add_all(attributes)

        await session.commit()
        await session.refresh(product)

        return await self.get_product_detail_by_id(product_id=product.id)

    async def update_product(self, product: Product, schema: UpdateProductRequestSchema) -> Product:
        # Get schema without attributes and images
        new_dict = {key: value for key, value in schema.model_dump(
        ).items() if not ("images" in key or "attributes" in key)}
        
        # Replace Values
        for field, value in new_dict.items():
            setattr(product, field, value)
        
        # TODO Images and Attributes
        
        await session.commit()
        await session.refresh(product)
        
        return await self.get_product_detail_by_id(product_id=product.id)

    @Transactional()
    async def delete_product(self, product_id: int):
        query = delete(Product).where(Product.id == product_id)
        await session.execute(query)

    @Transactional()
    async def __delete_product_images(self, product_id):
        query = delete(ProductImage).where(ProductImage.product_id == product_id)
        await session.execute(query)
