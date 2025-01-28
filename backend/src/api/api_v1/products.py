from typing import Annotated
from urllib.parse import urljoin

from fastapi import APIRouter, status, Depends, Request, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Product
from core.schemas.product import (
    ProductCreateUpdate,
    ProductResponse,
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
    request: Request,
):
    products = await crud.get_products(session=session)

    base_url = str(request.base_url)

    product_list = []

    for product in products:
        image_url = None
        if product.image:
            image_url = urljoin(base_url, product.image)
        product.image_url = image_url
        product_list.append(
            ProductListRead.model_validate(product)
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


@router.get("/{product_id}/", response_model=ProductDetailRead)
async def get_product(
    product: Annotated[
        Product,
        Depends(
            get_product_by_id_with_related_models,
        ),
    ],
    request: Request,
):
    base_url = str(request.base_url)

    image_url = None
    if product.image:
        image_url = urljoin(base_url, product.image)

    product.image_url = image_url

    return ProductDetailRead.model_validate(product)


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Annotated[Product, Depends(get_product_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> None:
    await crud.delete_product(session=session, product=product)


@router.put("/{product_id}/", response_model=ProductResponse)
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

    base_url = str(request.base_url)
    image_url = urljoin(base_url, file_path)

    return {"message": "Image uploaded successfully", "file_path": image_url}


@router.delete("/{product_id}/delete-image/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_image(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    product: Annotated[Product, Depends(get_product_by_id)],
):
    await crud.delete_product_image(
        session=session,
        product=product,
    )
