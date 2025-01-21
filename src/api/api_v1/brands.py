from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.brand import BrandRead
from crud import brands as crud


router = APIRouter(tags=["Brands"])


@router.get("/", response_model=list[BrandRead])
async def get_brands(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await crud.get_brands(session=session)
