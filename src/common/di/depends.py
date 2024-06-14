import inspect
from typing import Annotated, Any, Dict, List, Optional, Tuple, get_args, get_origin

from src.common.di.container import DependencyContainer
from src.common.di.exits import Exits


class Depends:
    __slots__ = (
        "_container",
        "_dependency",
        "_exits",
    )

    def __init__(self, dependency: Optional[Any] = None) -> None:
        self._dependency = dependency
        self._container = DependencyContainer()
        self._exits = Exits()

    async def resolve_async(self) -> Any:
        dependency = self._container[self._dependency]

        if callable(dependency):
            result = dependency()
            if inspect.isgenerator(result):
                self._exits.gens.append(result)
                result = next(result)
            elif inspect.iscoroutinefunction(result):
                result = await result
            elif inspect.isasyncgen(result):
                self._exits.gens.append(result)
                result = await anext(result)
        else:
            result = dependency

        return result

    def resolve_sync(self) -> Any:
        dependency = self._container[self._dependency]

        if callable(dependency):
            result = dependency()
            if inspect.isgenerator(result):
                self._exits.gens.append(result)
                result = next(result)
        else:
            result = dependency

        return result


def _resolve_sync_signature(
    signature: inspect.Signature,
) -> Tuple[List[Exits], Dict[str, Any]]:
    resolved_signature = {}
    exits = []
    for _, v in signature.parameters.items():
        param = v.default
        if isinstance(param, Depends):
            exits.append(param._exits)
            resolved_signature[v.name] = param.resolve_sync()
        if get_origin(v.annotation) is Annotated:
            metadata = v.annotation.__metadata__
            if metadata and isinstance(metadata[0], Depends):
                exits.append(metadata[0]._exits)
                resolved_signature[v.name] = metadata[0].resolve_sync()

    return exits, resolved_signature


async def _resolve_async_signature(
    signature: inspect.Signature,
) -> Tuple[List[Exits], Dict[str, Any]]:
    resolved_signature = {}
    exits = []
    for _, v in signature.parameters.items():
        param = v.default
        if isinstance(param, Depends):
            exits.append(param._exits)
            if param._dependency is None:
                param._dependency = v.annotation
            resolved_signature[v.name] = await param.resolve_async()

        if get_origin(v.annotation) is Annotated:
            metadata = v.annotation.__metadata__
            if metadata and isinstance(metadata[0], Depends):
                depends = metadata[0]
                exits.append(depends._exits)
                if depends._dependency is None:
                    depends._dependency = get_args(v.annotation)[0]
                resolved_signature[v.name] = await depends.resolve_async()
    
    return exits, resolved_signature
