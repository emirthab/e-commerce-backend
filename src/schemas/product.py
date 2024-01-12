from core.fastapi.schemas import TranslatableString

from pydantic import Field, BaseModel
from typing import Optional, List
from datetime import datetime


class ProductImageSchema(BaseModel):
    id: int = Field(...)
    image_path: str = Field(...)

class ProductAttributeSchema(BaseModel):
    attribute_id: int = Field(...)
    attribute_value_id: Optional[int] = Field(None)
    name: TranslatableString = Field(...)
    value: TranslatableString = Field(...)


class ProductDetailSchema(BaseModel):
    id: int = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    category_id: int = Field(...)
    images: List[ProductImageSchema] = Field(...)
    price: float = Field(...)
    attributes: List[ProductAttributeSchema] = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

    class Config:
        from_attributes = True

class ProductSchema(BaseModel):
    id: int = Field(...)
    title: str = Field(...)
    banner_image_path: Optional[str] = Field(...)
    price: float = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

    class Config:
        from_attributes = True

class GetProductsWithFiltersResponse(BaseModel):
    total_items: int = Field(...)
    page: int = Field(...)
    per_page: int = Field(...)
    data : List[ProductSchema] = Field(...)

class AddAdverAttributeSchema(BaseModel):
    attribute_id: int = Field(...)
    attribute_value_id: Optional[int] = Field(None)
    custom_value: Optional[str] = Field(None)


class CreateProductRequestSchema(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    images: List[int] = Field(...)
    price: float = Field(...)
    attributes: Optional[List[AddAdverAttributeSchema]] = Field(None)

class UpdateProductRequestSchema(CreateProductRequestSchema):
    ...
