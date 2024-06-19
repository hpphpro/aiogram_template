from aiogram import BaseMiddleware, Router

from src.core.logger import log
from src.middlewares.chat import ChatMiddleware
from src.middlewares.error import ErrorMiddleware
from src.middlewares.i18n import simple_locale_middleware

__all__ = (
    "ChatMiddleware",
    "simple_locale_middleware",
    "AutoInjectMiddleware",
    "ErrorMiddleware",
)


def setup_middlewares(
    router: Router, *middlewares: BaseMiddleware, is_outer: bool
) -> None:
    log.info(f'Setup {"outer" if is_outer else "inner"} middlewares... ')

    for middleware in middlewares:
        for observer in router.observers.values():
            if observer.event_name == 'update':
                continue
            if is_outer:
                observer.outer_middleware(middleware)
            else:
                observer.middleware(middleware)
