from __future__ import annotations

import inspect
from types import AsyncGeneratorType, GeneratorType
from typing import Any, List, Union


class Exits:
    __slots__ = ("gens",)

    def __init__(self) -> None:
        self.gens: List[
            Union[GeneratorType[Any, Any, Any], AsyncGeneratorType[Any, Any]]
        ] = []

    def __enter__(self) -> Exits:
        return self

    def __exit__(self) -> None:
        self.close()

    async def __aenter__(self) -> Exits:
        return self

    async def __aexit__(self) -> None:
        await self.aclose()

    def close(self) -> None:
        for gen in reversed(self.gens):
            if inspect.isgenerator(gen):
                next(gen, None)

    async def aclose(self) -> None:
        for gen in reversed(self.gens):
            if inspect.isgenerator(gen):
                next(gen, None)
            elif inspect.isasyncgen(gen):
                await anext(gen, None)
                