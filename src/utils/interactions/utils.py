from typing import Union, Optional, Any

from aiogram.types import CallbackQuery, Message
from aiogram.methods import DeleteMessage
from aiogram.exceptions import TelegramBadRequest


async def safe_delete_message(
        event: Union[CallbackQuery, Message],
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None
) -> Union[DeleteMessage, bool]:
    
    try:
        if all([chat_id, message_id]):
            msg = await event.bot.delete_message(
                chat_id=chat_id, # type: ignore
                message_id=message_id # type: ignore
            )
        else:
            if isinstance(event, Message):
                msg = await event.delete()
            else:
                msg = await event.message.delete()
    except TelegramBadRequest:
        return False
    
    return msg


async def safe_edit_message(
        event: Union[CallbackQuery, Message],
        text: str,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        **kwargs: Any
) -> Union[Message, bool]:
    
    try:
        if all([chat_id, message_id]):
            msg = await event.bot.edit_message_text(
                text=text,
                chat_id=chat_id, 
                message_id=message_id,
                **kwargs
            )
        else:
            if isinstance(event, Message):
                msg = await event.edit_text(
                    text=text,
                    **kwargs
                )
            else:
                msg = await event.message.edit_text(
                    text=text,
                    **kwargs
                )
    except TelegramBadRequest:
        return False
    
    return msg