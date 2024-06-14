import asyncio

from aiogram import Bot, types

from src.common.di import DependencyContainer
from src.common.extensions.chat import Chat
from src.common.extensions.pagination import Pagination
from src.core import (
    load_bot,
    load_dispatcher,
    load_settings,
    load_storage,
)
from src.core.logger import log
from src.database.core.connection import (
    create_sa_engine,
    create_sa_session_factory,
)
from src.database.gateway import DBGateway, get_gateway_lazy
from src.middlewares import (
    AutoInjectMiddleware,
    ChatMiddleware,
    ErrorMiddleware,
    setup_middlewares,
)
from src.routers import setup_routers
from src.routers.admin import setup_admin_router
from src.routers.client import setup_client_router


async def set_menu_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [types.BotCommand(command="/start", description="Start interacting with bot")]
    )


async def main() -> None:
    settings = load_settings()
    container = DependencyContainer()
    router = setup_routers(
        setup_client_router(),
        setup_admin_router(settings.bot.admins),
    )
    engine = create_sa_engine(
        settings.db.url,
        # for postgres only
        # pool_size=settings.db.connection_pool_size,
        # max_overflow=settings.db.connection_max_overflow,
        # pool_pre_ping=settings.db.connection_pool_pre_ping,
    )

    storage = load_storage(settings.redis)
    bot = load_bot(settings.bot)
    dp = load_dispatcher(storage)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_menu_commands(bot)

    session_factory = create_sa_session_factory(engine)
    container[DBGateway] = get_gateway_lazy(session_factory)

    dp.include_router(router)

    setup_middlewares(
        router,
        AutoInjectMiddleware(),  # if you want to use custom Dependency without inject decorator.
        ChatMiddleware(),
        ErrorMiddleware(with_backoff_error=True),
        is_outer=False,
    )

    log.info("Bot starting... ")
    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            chat=Chat(),
            pagination=Pagination(),
            # here you also can register anything you want as dependency.
            # NOTE: opened resources wont be closed automatically, so you need to use custom Depends or your own middleware
        )
    finally:
        await bot.session.close()
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
