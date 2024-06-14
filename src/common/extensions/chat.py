from collections import defaultdict
from typing import Any, Awaitable, Callable, Dict, List, Optional

CallbackType = Callable[..., Awaitable[Any]]


class Chat:
    def __init__(self) -> None:
        self.users: Dict[str, List[CallbackType]] = defaultdict(list)

    def get_callback(self, id: str) -> Optional[CallbackType]:
        stack = self.users.get(id, [])

        if len(stack) <= 1:
            return None
        
        stack.pop()

        return stack[-1]

    def set_callback(
        self, id: str, callback: CallbackType, from_start: bool = False
    ) -> None:
        if from_start:
            self.users[id] = [callback]
        else:
            self.users[id] += [callback]
