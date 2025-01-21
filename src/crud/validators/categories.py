from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Category
from utils.validator_helpers import validate_exists, validate_unique


async def validate_category_exists(
    session: AsyncSession,
    category_id: int,
):
    await validate_exists(
        session=session,
        model=Category,
        field_name="id",
        field_value=category_id,
        error_message=f"Category with id {category_id} does not exist.",
    )


async def validate_category_unique_name(
    session: AsyncSession,
    category_name: str,
    category_to_exclude: Category | None = None
):
    await validate_unique(
        session=session,
        model=Category,
        field_name="name",
        field_value=category_name,
        error_message=f"Category with name '{category_name}' already exists.",
        object_to_exclude=category_to_exclude,
    )
