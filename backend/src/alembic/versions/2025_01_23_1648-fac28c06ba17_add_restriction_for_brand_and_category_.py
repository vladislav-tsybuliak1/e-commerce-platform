"""Add restriction for brand and category deletion

Revision ID: fac28c06ba17
Revises: 76543d533f06
Create Date: 2025-01-23 16:48:10.819679

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fac28c06ba17"
down_revision: Union[str, None] = "76543d533f06"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "fk_product_category_id_category", "product", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_product_brand_id_brand", "product", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_product_category_id_category"),
        "product",
        "category",
        ["category_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        op.f("fk_product_brand_id_brand"),
        "product",
        "brand",
        ["brand_id"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_product_brand_id_brand"), "product", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_product_category_id_category"), "product", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_product_brand_id_brand", "product", "brand", ["brand_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_product_category_id_category",
        "product",
        "category",
        ["category_id"],
        ["id"],
    )
