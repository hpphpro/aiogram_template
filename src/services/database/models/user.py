from typing import Optional

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import (
    String,
    Boolean,
    BigInteger, 
)

from services.database.models.base import ModelWithTime, Base



class User(Base, ModelWithTime):

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True, 
        unique=True,
    )
    is_bot: Mapped[bool] = mapped_column(
        Boolean
    )
    first_name: Mapped[str] = mapped_column(String)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    language_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_premium: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    added_to_attachment_menu: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    can_join_groups: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    can_read_all_group_messages: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    supports_inline_queries: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
