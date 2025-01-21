from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: Annotated[str, MaxLen(63)]
    description: Annotated[str, MaxLen(1000)] | None = None


class CategoryCreateUpdate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
