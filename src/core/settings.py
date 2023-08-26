from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram.enums.parse_mode import ParseMode

import os
from functools import lru_cache
from typing import (
    Optional, 
    Union, 
    Dict, 
    Any,
    TypeAlias,
    Union,
    List,
)
from pathlib import Path


_StrPath: TypeAlias = Union[os.PathLike[str], str, Path]


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file='./.env', 
        env_file_encoding='utf-8', 
        case_sensitive=False
    )
    bot_token: str
    database_uri: str
    database_host: str
    database_port: int
    database_user: str
    database_name: str
    database_password: str
    admins: Optional[List[int]] = None
    parse_mode: Union[ParseMode, str] = ParseMode.HTML
    disable_web_page_preview: Optional[bool] = True
    protect_content: Optional[bool] = None
    redis_settings: Dict[str, Any] = {}

    @property
    def db_url(self) -> str:
        if 'sqlite' in self.database_uri:
            return self.database_uri.format(self.database_name)
        return self.database_uri.format(
            self.database_user,
            self.database_password,
            self.database_host,
            self.database_port,
            self.database_name,
        )

    @staticmethod
    def root_dir() -> Path:
        return Path(__file__).resolve().parent.parent.parent
    
    @classmethod
    def path(cls, *paths: _StrPath, base_path: Optional[_StrPath] = None) -> str:

        if base_path is None:
            base_path = cls.root_dir()
        
        return os.path.join(base_path, *paths)


@lru_cache(typed=True)
def load_settings() -> Settings: 
    return Settings() # type: ignore