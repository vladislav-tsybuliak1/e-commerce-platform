from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict


class BrandBase(BaseModel):
    name: Annotated[str, MaxLen(63)]
    description: Annotated[str, MaxLen(1000)] | None = None


class BrandCreateUpdate(BrandBase):
    pass


class BrandRead(BrandBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
