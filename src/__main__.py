
import asyncio

from aiogram.types import BotCommand

from src.core import bot, dp
from src.routers import router
from src.common.middlewares import (
    DatabaseMiddleware, 
)
from src.common.middlewares.i18n import simple_locale_middleware


async def on_startup() -> None:
    await bot.delete_webhook(drop_pending_updates=True)


async def register_bot_commands() -> None:
    commands = [
        BotCommand(command='/start', description='Bot start menu. Clears all the states')
    ]
    await bot.set_my_commands(commands)   


def register_routers() -> None:
    dp.include_router(router)


def register_middlewares() -> None:
    db_middleware = DatabaseMiddleware()
    simple_locale_middleware.setup(router)
    router.message.middleware.register(db_middleware)
    router.callback_query.middleware.register(db_middleware)


async def main() -> None:
    await on_startup()
    await register_bot_commands()
    register_middlewares()
    register_routers()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())