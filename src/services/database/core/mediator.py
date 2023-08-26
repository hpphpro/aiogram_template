from typing import Any, Optional, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from services.database.repositories.base import BaseRepository
from services.database.repositories import REPOSITORIES


class Mediator:
    
    def __init__(self) -> None:
        self._repositories: Dict[str, BaseRepository] = {}
        
    def add(
            self, 
            repository_instance: BaseRepository,  
            repository_name: Optional[str] = None
    ) -> None:
        
        self._repositories[
            repository_name or type(repository_instance).__name__.lower()
            ] = repository_instance
        
    def __getattr__(self, key: str) -> Any:
        
        if key in self._repositories:
            return self._repositories[key]
        
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")
    
    def __setattr__(self, key: str, value: Any) -> None:
        
        if key != '_repositories':
            self._repositories[key] = value
        else:
            super().__setattr__(key, value)


def build_mediator(session: AsyncSession) -> Mediator:
    
    meditor = Mediator()

    for repository in REPOSITORIES:
        meditor.add(repository(session))
        
    return meditor