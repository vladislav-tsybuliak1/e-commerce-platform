"""Add product table

Revision ID: 3c736c84102d
Revises: 271aa6c6121e
Create Date: 2025-01-17 15:42:32.055900

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3c736c84102d"
down_revision: Union[str, None] = "271aa6c6121e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "stock_unit",
            sa.Enum("KG", "G", "L", "ML", "PCS", "BOX", name="stockunitenum"),
            nullable=False,
        ),
        sa.Column(
            "weight_product",
            sa.Boolean(),
            server_default="false",
            nullable=False,
        ),
        sa.Column("stock_value", sa.Float(precision=2), nullable=False),
        sa.Column("stock_quantity", sa.Float(precision=2), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("brand_id", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "NOT (weight_product = TRUE AND stock_unit IN ('PCS', 'BOX'))",
            name=op.f("ck_product_weight_product_not_pcs_or_box"),
        ),
        sa.CheckConstraint(
            "price >= 0", name=op.f("ck_product_price_not_negative")
        ),
        sa.CheckConstraint(
            "stock_quantity >= 0",
            name=op.f("ck_product_stock_quantity_not_negative"),
        ),
        sa.CheckConstraint(
            "stock_value > 0", name=op.f("ck_product_stock_value_positive")
        ),
        sa.CheckConstraint(
            "weight_product = FALSE AND stock_quantity::INTEGER >= 0",
            name=op.f("ck_product_quantity_int_for_items"),
        ),
        sa.CheckConstraint(
            "weight_product = TRUE AND stock_quantity::FLOAT >= 0",
            name=op.f("ck_product_quantity_float_for_weight"),
        ),
        sa.ForeignKeyConstraint(
            ["brand_id"], ["brand.id"], name=op.f("fk_product_brand_id_brand")
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["category.id"],
            name=op.f("fk_product_category_id_category"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_product")),
    )


def downgrade() -> None:
    op.drop_table("product")
