from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base


ModelType = TypeVar("ModelType", bound=Base)


async def create_object(
    session: AsyncSession,
    object_create: BaseModel,
    model: type[ModelType],
) -> ModelType:
    obj = model(**object_create.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)

    return obj


async def get_objects(
    session: AsyncSession,
    model: type[ModelType],
) -> list[ModelType]:
    stmt = select(model).order_by(model.id)
    result: Result = await session.execute(stmt)
    objects = result.scalars().all()

    return list(objects)


async def get_object(
    session: AsyncSession,
    object_id: int,
    model: type[ModelType],
) -> ModelType | None:
    return await session.get(model, object_id)


async def delete_object(
    session: AsyncSession,
    obj: ModelType,
) -> None:
    await session.delete(obj)
    await session.commit()
