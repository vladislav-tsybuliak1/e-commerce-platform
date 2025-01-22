from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base


async def validate_exists(
    session: AsyncSession,
    model: type[Base],
    field_name: str,
    field_value,
    error_message: str,
):
    """
    Validates if a record exists in the database for the given model, field, and value.
    Raises HTTPException if the record is not found.
    """
    result = await session.execute(
        select(model).where(getattr(model, field_name) == field_value)
    )
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )


async def validate_unique(
    session: AsyncSession,
    model: type[Base],
    field_name: str,
    field_value,
    error_message: str,
    object_to_exclude: Base | None = None
):
    """
    Validates the uniqueness of a record in the database for the given model, field, and value.
    Raises HTTPException if the record already exists.
    """

    query = select(model).where(getattr(model, field_name) == field_value)

    if object_to_exclude is not None:
        query = query.where(
            getattr(model, "id") != getattr(object_to_exclude, "id")
        )

    result = await session.execute(query)
    record = result.scalar_one_or_none()

    if record is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )
