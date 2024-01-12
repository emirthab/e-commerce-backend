# Core imports
from fastapi.dependencies.utils import get_dependant
from fastapi import APIRouter, Request, Depends, Header, Query
from core.fastapi.middlewares import LocalizationRoute
from schemas import Langs

from core.fastapi.dependencies import (
    PermissionDependency,
    IsAuthenticated,
    IsAdmin,
    TranslateJsonResponse,
)

# App imports
from schemas import ProductSchema, ProductDetailSchema, CreateProductRequestSchema, UpdateProductRequestSchema, GetProductsWithFiltersResponse

from services import ProductServices
from models import ProductOrderType

# Python imports
from typing import List, Annotated, Optional, Any, Dict, Union

router = APIRouter(route_class=LocalizationRoute)


@router.get(
    "",
    response_model=GetProductsWithFiltersResponse,
)
async def get_product_with_filters(
        request: Request,
        page: int = 0,
        per_page: Annotated[int, Query(gt=1, le=20)] = 20,
        category_id: int = 0,
        search: Optional[str] = '',
        order_by: ProductOrderType = ProductOrderType.suggested,
        attrs: Dict[str, Union[Any, List[Any]]] = Query({}, example={'a_1':1, 'a_2_min':10, 'a_2_max': 1000, 'a_3': [2, 3, 4]})
):
    attributes = {key: value[0] if len(value) == 1 else value for key, value in attrs.items() if key.startswith("a_")}
    total_items, products = await ProductServices().get_products_with_filter(page=page, per_page=per_page, category_id=category_id, search=search, order_by=order_by, attributes=attributes)
    return {
        'total_items': total_items,
        'page': page,
        'per_page': per_page,
        'data': products
    }


@router.get(
    "/{product_id}",
    response_class=TranslateJsonResponse,
    response_model=ProductDetailSchema,
)
async def get_product_detail(
    request: Request,
    product_id: int,
    accept_language: Langs = Header("tr")
):
    return await ProductServices().get_product_detail_by_id(product_id=product_id)


@router.post(
    "",
    response_class=TranslateJsonResponse,
    response_model=ProductDetailSchema,
)
async def create_product(
    request: Request,
    category_id: int,
    schema: CreateProductRequestSchema,
    accept_language: Langs = Header("tr")
):
    return await ProductServices().create_product(category_id=category_id, schema=schema)


@router.put(
    "/{product_id}",
    response_class=TranslateJsonResponse,
    response_model=ProductDetailSchema,
)
async def update_product(
    request: Request,
    product_id: int,
    schema: UpdateProductRequestSchema,
    accept_language: Langs = Header("tr")
):
    product = await ProductServices().get_product_detail_by_id(product_id=product_id)
    return await ProductServices().update_product(product=product, schema=schema)


@router.delete(
    "/{product_id}",
)
async def delete_product(request: Request, product_id: int):
    return await ProductServices().delete_product(product_id=product_id)
