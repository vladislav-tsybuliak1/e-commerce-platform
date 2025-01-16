from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins import IntIdPkMixin


class Category(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(63), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
