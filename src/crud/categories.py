from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Category
from core.schemas.category import CategoryCreateUpdate
from utils.crud_helpers import (
    create_object,
    get_objects,
    get_object,
    delete_object,
    update_object,
)
from crud.validators.categories import validate_category_unique_name


async def create_category(
    session: AsyncSession,
    category_create: CategoryCreateUpdate,
) -> Category:
    await validate_category_unique_name(
        category_name=category_create.name,
        session=session,
    )

    return await create_object(
        session=session,
        object_create=category_create,
        model=Category,
    )


async def get_categories(session: AsyncSession) -> list[Category]:
    return await get_objects(session=session, model=Category)


async def get_category(
    session: AsyncSession,
    category_id: int,
) -> Category | None:
    return await get_object(
        session=session,
        object_id=category_id,
        model=Category,
    )


async def delete_category(
    session: AsyncSession,
    category: Category,
) -> None:
    await delete_object(session=session, obj=category)


async def update_category(
    session: AsyncSession,
    category: Category,
    category_update: CategoryCreateUpdate,
) -> Category:
    await validate_category_unique_name(
        category_name=category_update.name,
        session=session,
        category_to_exclude=category,
    )

    return await update_object(
        session=session,
        obj=category,
        obj_update=category_update,
    )
