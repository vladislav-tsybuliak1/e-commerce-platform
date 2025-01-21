from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base


ModelType = TypeVar("ModelType", bound=Base)


async def create(
    session: AsyncSession,
    object_create: BaseModel,
    model: type[ModelType],
) -> ModelType:
    obj = model(**object_create.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj
