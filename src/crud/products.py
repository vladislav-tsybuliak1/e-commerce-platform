from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from core.schemas.product import ProductCreateUpdate
from crud.validators.brands import validate_brand_exists
from crud.validators.categories import validate_category_exists
from crud.validators.products import validate_product_stock_unit
from crud.basic_cruds import create_object, get_objects, get_object


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
