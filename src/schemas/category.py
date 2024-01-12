from __future__ import annotations
from core.fastapi.schemas import TranslatableString
from pydantic import Field, BaseModel
from typing import Optional, List

from models import CustomInputType

class CategorySchema(BaseModel):
    id: int = Field(...)
    name: TranslatableString = Field(...)
    parent_id: Optional[int] = Field(...)
    sub_categories: List['CategorySchema'] = Field([])
    
    class Config:
        from_attributes = True

CategorySchema.model_rebuild()

class CategoryAttributeValueSchema(BaseModel):
    id: int = Field(...)
    name: TranslatableString = Field(...)

    class Config:
        from_attributes = True


class CategoryAttributeSchema(BaseModel):
    id: int = Field(...)
    name: TranslatableString = Field(...)
    is_required: bool = Field(...)
    allow_custom: bool = Field(...)
    allow_multiple: bool = Field(...)
    show_in_filters: bool = Field(...)
    custom_input_type: Optional[CustomInputType] = Field(...)
    input_prefix: Optional[str] = Field(...)
    values: Optional[List[CategoryAttributeValueSchema]] = Field(None)

    class Config:
        from_attributes = True