from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from core.settings import load_settings

settings = load_settings()

try:
    import redis.asyncio as aioredis  # type: ignore
    storage = RedisStorage(redis=aioredis.Redis(**settings.redis_settings))
except ImportError: 
    storage = MemoryStorage() # type: ignore

dp = Dispatcher(storage=storage)
bot = Bot(
    token=settings.bot_token,
    parse_mode=settings.parse_mode,
    disable_web_page_preview=settings.disable_web_page_preview,
    protect_content=settings.protect_content
)