from fastapi import APIRouter

from api.api_v1.categories import router as categories_router
from core.config import settings


router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(categories_router, prefix=settings.api.v1.categories)
