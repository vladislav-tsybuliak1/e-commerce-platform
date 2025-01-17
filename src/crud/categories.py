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
