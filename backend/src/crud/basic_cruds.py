from typing import TypeVar, Sequence

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, Result, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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
    order_by: Sequence[str] | None = None,
    related_models: Sequence[str] | None = None,
) -> list[ModelType]:
    stmt = select(model)

    if order_by:
        order_clauses = []
        for field in order_by:
            if field.startswith("-"):
                field_name = field[1:]
                order_clauses.append(desc(getattr(model, field_name)))
            else:
                order_clauses.append(asc(getattr(model, field)))
        stmt = stmt.order_by(*order_clauses)
    else:
        stmt = stmt.order_by(model.id)

    if related_models:
        for relation in related_models:
            stmt = stmt.options(joinedload(getattr(model, relation)))

    result: Result = await session.execute(stmt)
    objects = result.scalars().all()

    return list(objects)


async def get_object(
    session: AsyncSession,
    object_id: int,
    model: type[ModelType],
    related_models: Sequence[str] | None = None,
) -> ModelType | None:
    stmt = select(model).where(model.id == object_id)
    if related_models:
        for relation in related_models:
            stmt = stmt.options(joinedload(getattr(model, relation)))

    result: Result = await session.execute(stmt)

    return result.scalar_one_or_none()


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
    related_models: Sequence[str] | None = None,
) -> ModelType:
    obj = await get_object(
        session=session,
        object_id=object_id,
        model=model,
        related_models=related_models,
    )
    if obj:
        return obj
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=error_message,
    )
