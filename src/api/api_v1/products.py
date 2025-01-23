from typing import Annotated, cast
from urllib.parse import urljoin

from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.product import (
    ProductRead,
    ProductCreateUpdate,
    ProductResponse,
)
from crud import products as crud
from utils.enums import StockUnitEnum


router = APIRouter(tags=["Products"])


@router.get("/", response_model=list[ProductRead])
async def get_products(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    request: Request,
):
    products = await crud.get_products(session=session)

    base_url = str(request.base_url)

    product_list = []

    for product in products:
        image_url = None
        if product.image:
            image_url = urljoin(base_url, product.image)
        product_list.append(
            ProductRead(
                id=product.id,
                name=product.name,
                description=product.description,
                stock_unit=cast(StockUnitEnum, product.stock_unit),
                weight_product=product.weight_product,
                stock_value=product.stock_value,
                stock_quantity=product.stock_quantity,
                price=product.price,
                image_url=image_url,
                category=product.category.name,
                brand=product.brand.name,
            )
        )

    return product_list


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product_create: ProductCreateUpdate,
):
    product = await crud.create_product(
        session=session,
        product_create=product_create,
    )
    return product
