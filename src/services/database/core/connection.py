from typing import Optional

from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    AsyncEngine, 
    async_sessionmaker, 
    AsyncSession,
)

from src.core import settings


def async_engine() -> AsyncEngine:
    return create_async_engine(settings.db_url)


def create_session_factory(engine: Optional[AsyncEngine] = None) -> async_sessionmaker[AsyncSession]:
    
    if engine is None:
        engine = async_engine()
    
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


def async_session(session_factory: Optional[async_sessionmaker[AsyncSession]] = None) -> AsyncSession:
    if session_factory is None:
        session_factory = create_session_factory()
    return session_factory()
