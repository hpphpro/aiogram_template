from typing import Any, Dict

from src.common.di._meta import Singleton


class DependencyContainer(metaclass=Singleton):
    __slots__ = ("_dependencies",)

    def __init__(self) -> None:
        self._dependencies: Dict[Any, Any] = {}

    def register(self, key: Any, value: Any) -> None:
        self._dependencies[key] = value

    def get(self, key: Any) -> Any:
        return self._dependencies[key]

    def __getitem__(self, key: Any) -> Any:
        return self.get(key)

    def __setitem__(self, key: Any, value: Any) -> None:
        self._dependencies[key] = value
