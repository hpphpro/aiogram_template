from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage

from src.core.logger import log
from src.core.settings import BotSettings, RedisSettings


def load_storage(settings: Optional[RedisSettings] = None) -> BaseStorage:
    storage: BaseStorage

    if settings:
        import redis.asyncio as aioredis
        from aiogram.fsm.storage.redis import RedisStorage

        storage = RedisStorage(redis=aioredis.Redis(**settings.model_dump()))
    else:
        storage = MemoryStorage()

    log.info(f"Load storage: {type(storage)}...")
    return storage


def load_dispatcher(storage: Optional[BaseStorage] = None) -> Dispatcher:
    log.info("Load dispatcher...")
    return Dispatcher(storage=storage)


def load_bot(settings: BotSettings) -> Bot:
    log.info("Load bot... ")
    return Bot(
        token=settings.token,
        default=DefaultBotProperties(
            parse_mode=settings.parse_mode,
            protect_content=settings.protect_content,
            disable_notification=settings.disable_notifications,
            link_preview_is_disabled=settings.link_preview_is_disabled,
        ),
    )
