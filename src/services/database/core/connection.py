from typing import Optional

from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    AsyncEngine, 
    async_sessionmaker, 
    AsyncSession,
)

from core import settings


def async_engine() -> AsyncEngine:
    return create_async_engine(settings.db_url)


def async_session(engine: Optional[AsyncEngine] = None) -> AsyncSession:
    
    if engine is None:
        engine = async_engine()

    session = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)
    return session()
