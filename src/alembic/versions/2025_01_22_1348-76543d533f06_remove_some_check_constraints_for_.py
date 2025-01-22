"""Remove some check constraints for product table

Revision ID: 76543d533f06
Revises: c9c6d0c293e6
Create Date: 2025-01-22 13:48:44.617672

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "76543d533f06"
down_revision: Union[str, None] = "c9c6d0c293e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("product") as batch_op:
        batch_op.drop_constraint(
            op.f("ck_product_quantity_int_for_items"), type_="check"
        )
        batch_op.drop_constraint(
            op.f("ck_product_quantity_float_for_weight"), type_="check"
        )


def downgrade() -> None:
    with op.batch_alter_table("product") as batch_op:
        batch_op.create_check_constraint(
            op.f("ck_product_quantity_int_for_items"),
            condition="weight_product = FALSE AND stock_quantity::INTEGER >= 0",
        )
        batch_op.create_check_constraint(
            op.f("ck_product_quantity_float_for_weight"),
            condition="weight_product = TRUE AND stock_quantity::FLOAT >= 0",
        )
