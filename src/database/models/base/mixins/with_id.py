from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column


class ModelWithIDMixin:
    """Base model class that represents ID with an integer type"""

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

