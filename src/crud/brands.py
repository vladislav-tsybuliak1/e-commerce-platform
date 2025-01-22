from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Brand
from core.schemas.brand import BrandCreateUpdate
from crud.basic_cruds import (
    create_object,
    get_objects,
    get_object,
    delete_object,
    update_object,
)
from crud.validators.brands import validate_brand_unique_name


async def create_brand(
    session: AsyncSession,
    brand_create: BrandCreateUpdate,
) -> Brand:
    await validate_brand_unique_name(
        brand_name=brand_create.name,
        session=session,
    )

    return await create_object(
        session=session,
        object_create=brand_create,
        model=Brand,
    )


async def get_brands(session: AsyncSession) -> list[Brand]:
    return await get_objects(session=session, model=Brand)


async def get_brand(
    session: AsyncSession,
    brand_id: int,
) -> Brand | None:
    return await get_object(
        session=session,
        object_id=brand_id,
        model=Brand,
    )


async def delete_brand(
    session: AsyncSession,
    brand: Brand,
) -> None:
    await delete_object(session=session, obj=brand)


async def update_brand(
    session: AsyncSession,
    brand: Brand,
    brand_update: BrandCreateUpdate,
) -> Brand:
    await validate_brand_unique_name(
        session=session,
        brand_name=brand_update.name,
        brand_to_exclude=brand,
    )

    return await update_object(
        session=session,
        obj=brand,
        obj_update=brand_update,
    )