import uuid
from typing import Any, Awaitable, Callable, List, Optional

from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from src.core.logger import log


def on_hook_startup(
    url: str,
    path: str,
    certificate: Optional[types.InputFile] = None,
    ip_address: Optional[str] = None,
    max_connections: Optional[int] = None,
    allowed_updates: Optional[List[str]] = None,
    drop_pending_updates: Optional[bool] = None,
    secret_token: Optional[str] = None,
    request_timeout: Optional[int] = None,
) -> Callable[[Bot], Awaitable[None]]:
    async def _start_up(bot: Bot) -> None:
        await bot.set_webhook(
            url=f"{url.removesuffix("/")}/{path.removeprefix("/")}",
            certificate=certificate,
            ip_address=ip_address,
            max_connections=max_connections,
            allowed_updates=allowed_updates,
            drop_pending_updates=drop_pending_updates,
            secret_token=secret_token,
            request_timeout=request_timeout,
        )

    return _start_up


def init_webhook(
    dp: Dispatcher,
    bot: Bot,
    host: str,
    port: int,
    url: str = "https://aiogram.dev",
    url_path: str = "/webhook",
    certificate: Optional[types.InputFile] = None,
    ip_address: Optional[str] = None,
    max_connections: Optional[int] = None,
    allowed_updates: Optional[List[str]] = None,
    drop_pending_updates: Optional[bool] = None,
    secret_token: Optional[str] = None,
    request_timeout: Optional[int] = None,
    **dependencies: Any,
) -> None:
    if not secret_token:
        secret_token = uuid.uuid4().hex

    dp.startup.register(
        on_hook_startup(
            url=url,
            path=url_path,
            certificate=certificate,
            ip_address=ip_address,
            max_connections=max_connections,
            allowed_updates=allowed_updates or dp.resolve_used_update_types(),
            drop_pending_updates=drop_pending_updates,
            secret_token=secret_token,
            request_timeout=request_timeout,
        )
    )
    app = web.Application()

    SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=secret_token, **dependencies).register(
        app, path=url_path
    )

    setup_application(app, dp, bot=bot)
    log.info("Run bot webhook... ")

    web.run_app(app, host=host, port=port)
