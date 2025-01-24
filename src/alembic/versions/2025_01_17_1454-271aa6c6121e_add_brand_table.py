"""Add brand table

Revision ID: 271aa6c6121e
Revises: f19d63eec835
Create Date: 2025-01-17 14:54:44.586872

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "271aa6c6121e"
down_revision: Union[str, None] = "f19d63eec835"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "brand",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=63), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_brand")),
        sa.UniqueConstraint("name", name=op.f("uq_brand_name")),
    )


def downgrade() -> None:
    op.drop_table("brand")
