from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Category


async def validate_category_exists(
    session: AsyncSession,
    category_id: int,
):
    result = await session.execute(
        select(Category).where(Category.id == category_id)
    )
    category = result.scalar_one_or_none()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} does not exists",
        )


async def validate_category_unique_name(
    session: AsyncSession,
    category_name: str,
):
    result = await session.execute(select(Category).where(Category.name == category_name))
    category = result.scalar_one_or_none()
    if category is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name {category_name} already exists.",
        )
