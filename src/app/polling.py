from typing import Any, Awaitable, Callable, Optional

from aiogram import Bot, Dispatcher

from src.core.logger import log


def on_startup(
    *bots: Bot,
    drop_pending_updates: Optional[bool] = None,
) -> Callable[[], Awaitable[None]]:
    async def _startup() -> None:
        for bot in bots:
            await bot.delete_webhook(drop_pending_updates=drop_pending_updates)

    return _startup


def init_polling(
    dp: Dispatcher,
    *bots: Bot,
    drop_pending_updates: Optional[bool] = None,
    **dependencies: Any,
) -> None:
    log.info("Run bot polling... ")
    dp.startup.register(on_startup(*bots, drop_pending_updates=drop_pending_updates))
    dp.run_polling(
        *bots, allowed_updates=dp.resolve_used_update_types(), **dependencies
    )
