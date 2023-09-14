from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram import types
from aiogram.types import TelegramObject

from src.common.middlewares.i18n import gettext as _



class ErrorMiddlware(BaseMiddleware):
    
    async def __call__(
            self, 
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
            event: TelegramObject, 
            data: Dict[str, Any]
    ) -> Any:
        
        from src.routers.error import logger
        from src.utils.interactions.utils import safe_delete_message
        from src.utils.text import ERROR_RESTART_MESSAGE
        
        try:
            return await handler(event, data)
        except Exception as e:
            logger.error(f'{e}')
            await safe_delete_message(event) # type: ignore
            if isinstance(event, types.CallbackQuery):
                await event.message.answer(_(ERROR_RESTART_MESSAGE))
            if isinstance(event, types.Message):
                await event.answer(_(ERROR_RESTART_MESSAGE))
            