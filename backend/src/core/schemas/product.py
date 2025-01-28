from typing import Annotated

from annotated_types import MaxLen, Gt, Ge
from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict

from core.schemas.brand import BrandRead
from core.schemas.category import CategoryRead
from utils.enums import StockUnitEnum


class ProductBase(BaseModel):
    name: Annotated[str, MaxLen(255)]
    description: Annotated[str | None, MaxLen(1000)] = None
    stock_unit: StockUnitEnum
    weight_product: bool = False
    stock_value: Annotated[float, Gt(0)]
    stock_quantity: Annotated[float, Ge(0)]
    price: Annotated[int, Ge(0)]


class ProductCreateUpdate(ProductBase):
    category_id: int
    brand_id: int


class ProductListRead(ProductBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    image_url: str | None
    category_id: int
    brand_id: int


class ProductDetailRead(ProductBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    image_url: str | None
    category: CategoryRead
    brand: BrandRead


class ProductResponse(ProductBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    image: str | None
    category_id: int
    brand_id: int


class ProductImageUpload(BaseModel):
    image: UploadFile
