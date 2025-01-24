from fastapi import APIRouter

from api.api_v1.categories import router as categories_router
from api.api_v1.brands import router as brands_router
from api.api_v1.products import router as products_router
from core.config import settings


router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(categories_router, prefix=settings.api.v1.categories)
router.include_router(brands_router, prefix=settings.api.v1.brands)
router.include_router(products_router, prefix=settings.api.v1.products)
