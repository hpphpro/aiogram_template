
import asyncio
from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import AsyncEngine

from src.core import (
    load_bot, 
    load_dispatcher, 
    load_storage,
    load_settings,
)
from src.database.core.connection import async_engine
from src.routers import router
from src.common.middlewares import (
    DatabaseMiddleware, 
    TrottlingMiddleware,
    ErrorMiddlware,
)
from src.common.middlewares.i18n import simple_locale_middleware
from src.utils.interactions import Chat, PaginationMediator


async def on_startup(bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)


async def register_bot_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command='/start', description='Bot start menu. Clears all the states')
    ]
    await bot.set_my_commands(commands)   


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(router)


def register_middlewares(
        storage: BaseStorage,
        engine: Optional[AsyncEngine] = None
) -> None:

    if not isinstance(storage, MemoryStorage):
        trottle = TrottlingMiddleware(storage)
        router.message.outer_middleware(trottle)
        router.callback_query.outer_middleware(trottle)
    error = ErrorMiddlware()
    db_middleware = DatabaseMiddleware(engine)
    simple_locale_middleware.setup(router)
    router.message.middleware.register(db_middleware)
    router.callback_query.middleware.register(db_middleware)
    router.message.outer_middleware.register(error)
    router.callback_query.outer_middleware.register(error)


async def main() -> None:
    settings = load_settings()
    bot = load_bot(settings)
    storage = load_storage(settings)
    dp = load_dispatcher(storage)
    engine = async_engine()
    await on_startup(bot)
    await register_bot_commands(bot)
    register_middlewares(storage, engine)
    register_routers(dp)
    await dp.start_polling(
        bot, 
        allowed_updates=dp.resolve_used_update_types(),
        chat=Chat(),
        pagination=PaginationMediator()
    )


if __name__ == '__main__':
    asyncio.run(main())
