from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Category
from core.schemas.category import CategoryRead, CategoryCreateUpdate
from crud import categories as crud


router = APIRouter(tags=["Categories"])


@router.get("/", response_model=list[CategoryRead])
async def get_categories(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await crud.get_categories(session=session)


@router.post(
    "/",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    category_create: CategoryCreateUpdate,
) -> Category:
    category = await crud.create_category(
        session=session,
        category_create=category_create,
    )
    return category
