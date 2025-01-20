from typing import Annotated

from fastapi import HTTPException, status
from fastapi.params import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Category
from crud import categories as categories_crud


async def get_category_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    category_id: Annotated[int, Path]
) -> Category:
    category = await categories_crud.get_category(
        session=session,
        category_id=category_id,
    )
    if category:
        return category
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Category {category_id} not found!",
    )
