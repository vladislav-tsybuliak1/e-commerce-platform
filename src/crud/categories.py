from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Category
from core.schemas.category import CategoryCreateUpdate
from crud.validators import validate_category_unique_name


async def create_category(
    session: AsyncSession,
    category_create: CategoryCreateUpdate,
) -> Category:
    await validate_category_unique_name(
        category_name=category_create.name,
        session=session,
    )

    category = Category(**category_create.model_dump())
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def get_categories(session: AsyncSession) -> list[Category]:
    stmt = select(Category).order_by(Category.id)
    result: Result = await session.execute(stmt)
    categories = result.scalars().all()

    return list(categories)


async def get_category(
    session: AsyncSession,
    category_id: int,
) -> Category | None:
    return await session.get(Category, category_id)


async def delete_category(
    session: AsyncSession,
    category: Category,
) -> None:
    await session.delete(category)
    await session.commit()


async def update_category(
    session: AsyncSession,
    category: Category,
    category_update: CategoryCreateUpdate,
) -> Category:
    await validate_category_unique_name(
        category_name=category_update.name,
        session=session,
    )
    for attr, value in category_update.model_dump().items():
        setattr(category, attr, value)
    await session.commit()
    await session.refresh(category)
    return category
