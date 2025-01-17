from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins import IntIdPkMixin


if TYPE_CHECKING:
    from core.models.product import Product


class Category(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(63), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        default=None,
        server_default=None,
    )

    # Relationships
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
    )
