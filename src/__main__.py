from typing import Awaitable, Callable, List, Mapping

from aiogram import Bot, types

from src.app import init_polling
from src.common.di import DependencyContainer
from src.common.extensions.chat import Chat
from src.common.extensions.pagination import Pagination
from src.core import (
    load_bot,
    load_dispatcher,
    load_settings,
    load_storage,
)
from src.database.core.connection import (
    create_sa_engine,
    create_sa_session_factory,
)
from src.database.gateway import DBGateway, get_gateway_lazy
from src.middlewares import (
    ChatMiddleware,
    ErrorMiddleware,
    setup_middlewares,
)
from src.routers import setup_routers
from src.routers.admin import setup_admin_router
from src.routers.client import setup_client_router
from src.routers.examples import setup_example_router


def set_menu_commands(
    bots_settings: Mapping[Bot, List[types.BotCommand]],
) -> Callable[[], Awaitable[None]]:
    async def _startup() -> None:
        for bot, commands in bots_settings.items():
            await bot.set_my_commands(commands=commands)

    return _startup


def on_shutdown(*bots: Bot) -> Callable[[], Awaitable[None]]:
    async def _startup() -> None:
        for bot in bots:
            await bot.session.close()

    return _startup


def main() -> None:
    settings = load_settings()
    container = DependencyContainer()
    router = setup_routers(
        setup_client_router(),
        setup_admin_router(settings.bot.admins),
        setup_example_router(),  # TODO: delete it, it just for test
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
    dp.shutdown.register(on_shutdown(bot))
    dp.startup.register(
        set_menu_commands(
            {
                bot: [
                    types.BotCommand(
                        command="/start", description="Start interacting with bot"
                    )
                ]
            }
        )
    )
    session_factory = create_sa_session_factory(engine)
    container[DBGateway] = get_gateway_lazy(session_factory)

    dp.include_router(router)
    setup_middlewares(
        router,
        ChatMiddleware(
            wrap_injection=True  # if you want to use custom Dependency without inject decorator.
        ),
        ErrorMiddleware(with_backlog_error=True),
        is_outer=False,
    )

    try:
        init_polling(
            dp,
            bot,
            drop_pending_updates=True,
            chat=Chat(),
            pagination=Pagination(),
            # here you also can register anything you want as dependency.
            # NOTE: opened resources wont be closed automatically, so you need to use custom Depends or your own middleware
        )
    finally:
        engine.sync_engine.dispose()


if __name__ == "__main__":
    main()
