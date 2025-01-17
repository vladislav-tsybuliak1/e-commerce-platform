"""Add image field to product table

Revision ID: c9c6d0c293e6
Revises: 8f9cfdd27d76
Create Date: 2025-01-17 16:28:57.863874

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c9c6d0c293e6"
down_revision: Union[str, None] = "8f9cfdd27d76"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "product", sa.Column("image", sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("product", "image")
