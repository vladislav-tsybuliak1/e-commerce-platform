from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Brand
from utils.validator_helpers import validate_exists, validate_unique


async def validate_brand_exists(
    session: AsyncSession,
    brand_id: int,
):
    await validate_exists(
        session=session,
        model=Brand,
        field_name="id",
        field_value=brand_id,
        error_message=f"Brand with id {brand_id} does not exist.",
    )


async def validate_brand_unique_name(
    session: AsyncSession,
    brand_name: str,
    brand_to_exclude: Brand | None = None,
):
    await validate_unique(
        session=session,
        model=Brand,
        field_name="name",
        field_value=brand_name,
        error_message=f"Brand with name '{brand_name}' already exists.",
        object_to_exclude=brand_to_exclude,
    )
