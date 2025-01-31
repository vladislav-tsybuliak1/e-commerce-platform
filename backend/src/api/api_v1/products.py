from typing import Annotated
from urllib.parse import urljoin

from fastapi import APIRouter, status, Depends, Request, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Product
from core.schemas.product import (
    ProductCreateUpdate,
    ProductListRead,
    ProductDetailRead,
)
from crud import products as crud
from crud.dependencies import (
    get_product_by_id,
    get_product_by_id_with_related_models,
)


router = APIRouter(tags=["Products"])


@router.get("/", response_model=list[ProductListRead])
async def get_products(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await crud.get_products(session=session)


@router.post(
    "/",
    response_model=ProductListRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product_create: ProductCreateUpdate,
):
    return await crud.create_product(
        session=session,
        product_create=product_create,
    )


@router.get("/{product_id}/", response_model=ProductDetailRead)
async def get_product(
    product: Annotated[
        Product,
        Depends(
            get_product_by_id_with_related_models,
        ),
    ],
):
    return product


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Annotated[Product, Depends(get_product_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> None:
    await crud.delete_product(session=session, product=product)


@router.put("/{product_id}/", response_model=ProductListRead)
async def update_product(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product: Annotated[Product, Depends(get_product_by_id)],
    product_update: ProductCreateUpdate,
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.post("/{product_id}/upload-image/")
async def upload_product_image(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product: Annotated[Product, Depends(get_product_by_id)],
    request: Request,
    image: UploadFile = File(
        ...,
        description="The image file to upload (only png, jpeg, jpg are allowed)",
        media_type="image/jpeg, image/png",
    ),
):
    file_path = await crud.upload_product_image(
        session=session,
        product=product,
        image=image,
    )

    return {"message": "Image uploaded successfully", "file_path": file_path}


@router.delete("/{product_id}/delete-image/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_image(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product: Annotated[Product, Depends(get_product_by_id)],
):
    await crud.delete_product_image(
        session=session,
        product=product,
    )
