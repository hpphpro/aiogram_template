from typing import Any, List, Optional, Union

from aiogram.filters import Filter 
from aiogram import types

from src.core import load_settings


class IsAdmin(Filter):

    def __init__(self, admins: Optional[List[int]] = load_settings().admins) -> None:
        self.admins = admins or []

    async def __call__(
            self, event: Union[types.CallbackQuery, types.Message]
    ) -> Any:
        
        return event.from_user.id in self.admins # type: ignore
