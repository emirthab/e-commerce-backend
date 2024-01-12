from fastapi import APIRouter

# Router İmports
from .auth import router as auth_router
from .user import router as user_router
from .file import router as file_router
from .category import router as category_router
from .product import router as product_router
from .translations import router as translation_router
from .events import router as events_router
from .recommender import router as recommender_router

router = APIRouter()

# Api Endpoint Definitions
router.include_router(auth_router, prefix='/api/auth', tags=['auth'])
router.include_router(user_router, prefix='/api/user', tags=['user'])
router.include_router(product_router, prefix='/api/product', tags=['product'])
router.include_router(category_router, prefix='/api/category', tags=['category'])
router.include_router(file_router, prefix='/api/file', tags=['file'])
router.include_router(translation_router, prefix='/api/translations', tags=['translations'])
router.include_router(recommender_router, prefix='/api/recommender', tags=['recommender'])
router.include_router(events_router, prefix='/api/events', tags=['events'])

__all__ = ["router"]
