from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base
from src.database.models.base.mixins import ModelWithTimeMixin


class User(ModelWithTimeMixin, Base):
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True,
    )
    is_bot: Mapped[bool]
    first_name: Mapped[str]
    username: Mapped[Optional[str]] = mapped_column(nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    language_code: Mapped[Optional[str]] = mapped_column(nullable=True)
    is_premium: Mapped[Optional[bool]] = mapped_column(nullable=True)
    added_to_attachment_menu: Mapped[Optional[bool]] = mapped_column(nullable=True)
    can_join_groups: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    can_read_all_group_messages: Mapped[Optional[bool]] = mapped_column(nullable=True)
    supports_inline_queries: Mapped[Optional[bool]] = mapped_column(nullable=True)
    can_connect_to_business: Mapped[Optional[bool]] = mapped_column(nullable=True)
