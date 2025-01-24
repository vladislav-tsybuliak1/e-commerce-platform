import os

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from core.schemas.product import ProductCreateUpdate
from crud.validators.brands import validate_brand_exists
from crud.validators.categories import validate_category_exists
from crud.validators.products import (
    validate_product_stock_unit,
    validate_image_content_type,
    validate_product_has_image,
    validate_product_does_not_have_image,
)
from crud.basic_cruds import (
    create_object,
    get_objects,
    get_object,
    delete_object,
    update_object,
)
from utils.image_paths import product_image_file_path
from utils.image_resize import resize_image


async def create_product(
    session: AsyncSession,
    product_create: ProductCreateUpdate,
) -> Product:
    await validate_category_exists(
        session=session,
        category_id=product_create.category_id,
    )
    await validate_brand_exists(
        session=session,
        brand_id=product_create.brand_id,
    )
    validate_product_stock_unit(product_create_update=product_create)

    return await create_object(
        session=session,
        object_create=product_create,
        model=Product,
    )


async def get_products(session: AsyncSession) -> list[Product]:
    return await get_objects(
        session=session,
        model=Product,
        related_models=["category", "brand"],
    )


async def get_product(
    session: AsyncSession,
    product_id: int,
) -> Product | None:
    return await get_object(
        session=session,
        object_id=product_id,
        model=Product,
        related_models=["category", "brand"],
    )


async def delete_product(
    session: AsyncSession,
    product: Product,
) -> None:
    if product.image:
        if os.path.exists(product.image):
            os.remove(product.image)

    await delete_object(session=session, obj=product)


async def update_product(
    session: AsyncSession,
    product: Product,
    product_update: ProductCreateUpdate,
) -> Product:
    await validate_category_exists(
        session=session,
        category_id=product_update.category_id,
    )
    await validate_brand_exists(
        session=session,
        brand_id=product_update.brand_id,
    )
    validate_product_stock_unit(product_create_update=product_update)

    return await update_object(
        session=session,
        obj=product,
        obj_update=product_update,
    )


async def upload_product_image(
    session: AsyncSession,
    product: Product,
    image: UploadFile,
    max_file_size: int = 1 * 1024 * 1024,  # 1 MB
) -> str:
    validate_product_does_not_have_image(product)
    validate_image_content_type(image)

    # Generate file_path
    file_path = product_image_file_path(product, image.filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save the image temporarily
    temp_path = file_path + ".temp"
    with open(temp_path, "wb") as file:
        content = await image.read()
        file.write(content)

    # Resize image
    resize_image(
        temp_path=temp_path,
        file_path=file_path,
        max_file_size=max_file_size,
    )

    # Update the product
    product.image = file_path
    session.add(product)
    await session.commit()
    await session.refresh(product)

    return str(product.image)


async def delete_product_image(
    session: AsyncSession,
    product: Product,
):
    validate_product_has_image(product)

    if os.path.exists(product.image):
        os.remove(product.image)

    product.image = None
    session.add(product)
    await session.commit()
    await session.refresh(product)
