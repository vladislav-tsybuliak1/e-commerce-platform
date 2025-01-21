from typing import TypeVar, Annotated

from fastapi import Path, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base


ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


async def create_object(
    session: AsyncSession,
    object_create: SchemaType,
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


async def update_object(
    session: AsyncSession,
    obj: ModelType,
    obj_update: SchemaType,
) -> ModelType:
    for attr, value in obj_update.model_dump().items():
        setattr(obj, attr, value)
    await session.commit()
    await session.refresh(obj)

    return obj


async def get_object_by_id(
    session: AsyncSession,
    object_id: int,
    model: type[ModelType],
    error_message: str,
) -> ModelType:
    obj = await get_object(
        session=session,
        object_id=object_id,
        model=model,
    )
    if obj:
        return obj
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=error_message,
    )
