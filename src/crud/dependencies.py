from typing import Annotated

from fastapi.params import Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Category, Brand
from utils.crud_helpers import get_object_by_id



async def get_category_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    category_id: Annotated[int, Path]
) -> Category:
    return await get_object_by_id(
        session=session,
        object_id=category_id,
        model=Category,
        error_message=f"Category with ID {category_id} is not found.",
    )


async def get_brand_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    brand_id: Annotated[int, Path]
) -> Brand:
    return await get_object_by_id(
        session=session,
        object_id=brand_id,
        model=Brand,
        error_message=f"Brand with ID {brand_id} is not found.",
    )
