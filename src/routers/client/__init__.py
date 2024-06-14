from aiogram import Router
from aiogram.enums.chat_type import ChatType
from aiogram.filters import CommandStart

from src.filters.client import IsChatType
from src.routers.client.start import start_message


def setup_client_router() -> Router:
    router = Router(name="client")
    # TODO setup client handlers
    router.message.register(start_message, CommandStart(), IsChatType(ChatType.PRIVATE))

    return router
