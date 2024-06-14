from __future__ import annotations

from typing import Any, Dict


class Singleton(type):
    __instances: Dict[Singleton, Singleton] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]
