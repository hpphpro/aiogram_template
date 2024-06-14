from typing import List, Union

from aiogram import types
from aiogram.filters import Filter


class IsAdmin(Filter):
    def __init__(self, admins: List[int]) -> None:
        self._admins = admins

    async def __call__(self, event: Union[types.CallbackQuery, types.Message]) -> bool:
        user_id = 0
        if isinstance(event, types.Message):
            user_id = event.from_user.id if event.from_user else 0
        if isinstance(event, types.CallbackQuery):
            user_id = event.from_user.id

        return user_id in self._admins
