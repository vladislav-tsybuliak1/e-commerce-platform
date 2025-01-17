from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Text,
    Enum as SQLAlchemyEnum,
    Float,
    Integer,
    ForeignKey,
    CheckConstraint,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins import IntIdPkMixin


if TYPE_CHECKING:
    from core.models.category import Category
    from core.models.brand import Brand


class StockUnitEnum(str, PyEnum):
    KG = "KG"
    G = "G"
    L = "L"
    ML = "ML"
    PCS = "PCS"
    BOX = "BOX"


class Product(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        default=None,
        server_default=None,
    )
    stock_unit: Mapped[str] = mapped_column(
        SQLAlchemyEnum(StockUnitEnum),
        nullable=False,
    )
    weight_product: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    stock_value: Mapped[float] = mapped_column(
        Float(precision=2),
        nullable=False,
    )
    stock_quantity: Mapped[float] = mapped_column(
        Float(precision=2),
        nullable=False,
    )
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    # Foreign Key relationship
    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"),
        nullable=False,
    )
    brand_id: Mapped[int] = mapped_column(ForeignKey("brand.id"), nullable=False)

    # Relationships
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products",
    )
    brand: Mapped["Brand"] = relationship(
        "Brand",
        back_populates="products",
    )

    __table_args__ = (
        CheckConstraint("price >= 0", name="price_not_negative"),
        CheckConstraint(
            "stock_quantity >= 0",
            name="stock_quantity_not_negative",
        ),
        CheckConstraint("stock_value > 0", name="stock_value_positive"),
        CheckConstraint(
            "weight_product = TRUE AND stock_quantity::FLOAT >= 0",
            name="quantity_float_for_weight"
        ),
        CheckConstraint(
            "weight_product = FALSE AND stock_quantity::INTEGER >= 0",
            name="quantity_int_for_items"
        ),
        CheckConstraint(
            "NOT (weight_product = TRUE AND stock_unit IN ('PCS', 'BOX'))",
            name="weight_product_not_pcs_or_box",
        ),
    )
