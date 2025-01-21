from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Brand
from core.schemas.brand import BrandCreateUpdate
from crud.basic_helpers import (
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
