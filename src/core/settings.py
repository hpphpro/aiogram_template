import os
from pathlib import Path
from typing import Final, List, Literal, Optional, Union

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(raise_error_if_not_found=True))

_StrPath = Union[os.PathLike[str], str, Path]


LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
PROJECT_NAME = os.getenv("PROJECT_NAME", "MyBot")

LOGGING_FORMAT: Final[str] = "%(asctime)s %(name)s %(levelname)s -> %(message)s"
DATETIME_FORMAT: Final[str] = "%Y.%m.%d %H:%M"


def root_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def path(*paths: _StrPath, base_path: Optional[_StrPath] = None) -> str:
    if base_path is None:
        base_path = root_dir()

    return os.path.join(base_path, *paths)


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="DB_",
        extra="ignore",
    )

    uri: str = ""
    name: str = ""
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    connection_pool_size: int = 10
    connection_max_overflow: int = 90
    connection_pool_pre_ping: bool = True

    @property
    def url(self) -> str:
        if "sqlite" in self.uri:
            return self.uri.format(self.name)
        return self.uri.format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.name,
        )


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="BOT_",
        extra="ignore",
    )

    token: str = ""
    admins: List[int] = []
    parse_mode: Literal["HTML", "Markdown", "MarkdownV2"] = "HTML"
    disable_notifications: Optional[bool] = True
    link_preview_is_disabled: Optional[bool] = True
    protect_content: Optional[bool] = None


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="REDIS_",
        extra="ignore",
    )
    host: str = "127.0.0.1"
    port: int = 6379


class Settings(BaseSettings):
    bot: BotSettings
    redis: RedisSettings
    db: DatabaseSettings


def load_settings(
    bot_settings: Optional[BotSettings] = None,
    redis_settings: Optional[RedisSettings] = None,
    db_settings: Optional[DatabaseSettings] = None,
) -> Settings:
    return Settings(
        bot=bot_settings or BotSettings(),
        redis=redis_settings or RedisSettings(),
        db=db_settings or DatabaseSettings(),
    )
