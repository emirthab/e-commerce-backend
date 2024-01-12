# Core imports
from fastapi import APIRouter, Request, Depends, Header

from core.fastapi.middlewares import LocalizationRoute
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAuthenticated,
    IsAdmin,
    TranslateJsonResponse
)

# App imports
from schemas import (
    CategorySchema,
    CategoryAttributeSchema,
    Langs
)

from services import CategoryServices

# Python imports
from typing import List

router = APIRouter(route_class=LocalizationRoute)


@router.get(
    "",
    response_class=TranslateJsonResponse,
    response_model=List[CategorySchema],
)
async def get_category_tree(
        request: Request,
        accept_language: Langs = Header("tr")
):
    categories = await CategoryServices().get_category_tree()
    return categories


@router.get(
    "/{category_id}/attributes",
    response_class=TranslateJsonResponse,
    response_model=List[CategoryAttributeSchema],
)
async def get_category_attributes(
        request: Request,
        category_id: int,
        accept_language: Langs = Header("tr")
):
    category_attr = await CategoryServices().get_category_attributes(category_id=category_id)
    return category_attr.attributes
