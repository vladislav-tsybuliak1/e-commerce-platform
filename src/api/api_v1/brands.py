from typing import Annotated

from fastapi import APIRouter, Depends,status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Brand
from core.schemas.brand import BrandRead, BrandCreateUpdate
from crud import brands as crud
from crud.dependencies import get_brand_by_id

router = APIRouter(tags=["Brands"])


@router.get("/", response_model=list[BrandRead])
async def get_brands(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await crud.get_brands(session=session)


@router.post(
    "/",
    response_model=BrandRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_brand(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    brand_create: BrandCreateUpdate,
) -> Brand:
    brand = await crud.create_brand(
        session=session,
        brand_create=brand_create,
    )
    return brand


@router.get("/{brand_id}/", response_model=BrandRead)
async def get_brand(
    brand: Annotated[Brand, Depends(get_brand_by_id)],
):
    return brand
