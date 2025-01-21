from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Text,
    Enum,
    Integer,
    ForeignKey,
    CheckConstraint,
    Boolean,
    DOUBLE_PRECISION,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins import IntIdPkMixin
from utils.enums import StockUnitEnum


if TYPE_CHECKING:
    from core.models.category import Category
    from core.models.brand import Brand


class Product(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        default=None,
        server_default=None,
    )
    stock_unit: Mapped[str] = mapped_column(
        Enum(StockUnitEnum),
        nullable=False,
    )
    weight_product: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    stock_value: Mapped[float] = mapped_column(
        DOUBLE_PRECISION,
        nullable=False,
    )
    stock_quantity: Mapped[float] = mapped_column(
        DOUBLE_PRECISION,
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
    image: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        default=None,
        server_default=None,
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
            name="quantity_float_for_weight",
        ),
        CheckConstraint(
            "weight_product = FALSE AND stock_quantity::INTEGER >= 0",
            name="quantity_int_for_items",
        ),
        CheckConstraint(
            "NOT (weight_product = TRUE AND stock_unit IN ('PCS', 'BOX'))",
            name="weight_product_not_pcs_or_box",
        ),
    )
