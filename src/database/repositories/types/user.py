from typing import Optional, TypedDict

from typing_extensions import NotRequired, Required


class CreateUserType(TypedDict):
    id: Required[int]
    is_bot: Required[bool]
    first_name: Required[str]
    username: NotRequired[Optional[str]]
    last_name: NotRequired[Optional[str]]
    language_code: NotRequired[Optional[str]]
    is_premium: NotRequired[Optional[bool]]
    added_to_attachment_menu: NotRequired[Optional[bool]]
    can_join_groups: NotRequired[Optional[bool]]
    can_read_all_group_messages: NotRequired[Optional[bool]]
    supports_inline_queries: NotRequired[Optional[bool]]
    can_connect_to_business: NotRequired[Optional[bool]]


class UpdateUserType(TypedDict):
    is_bot: NotRequired[bool]
    first_name: NotRequired[str]
    username: NotRequired[Optional[str]]
    last_name: NotRequired[Optional[str]]
    language_code: NotRequired[Optional[str]]
    is_premium: NotRequired[Optional[bool]]
    added_to_attachment_menu: NotRequired[Optional[bool]]
    can_join_groups: NotRequired[Optional[bool]]
    can_read_all_group_messages: NotRequired[Optional[bool]]
    supports_inline_queries: NotRequired[Optional[bool]]
    can_connect_to_business: NotRequired[Optional[bool]]
