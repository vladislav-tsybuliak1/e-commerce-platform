from typing import Annotated

from annotated_types import MaxLen, Gt, Ge
from pydantic import BaseModel, ConfigDict

from utils.enums import StockUnitEnum


class ProductBase(BaseModel):
    name: Annotated[str, MaxLen(255)]
    description: Annotated[str | None, MaxLen(1000)] = None
    stock_unit: StockUnitEnum
    weight_product: bool = False
    stock_value: Annotated[float, Gt(0)]
    stock_quantity: Annotated[float, Ge(0)]
    price: Annotated[int, Ge(0)]
    category_id: int
    brand_id: int


class ProductCreateUpdate(ProductBase):
    pass


class ProductRead(ProductBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    image: str | None
