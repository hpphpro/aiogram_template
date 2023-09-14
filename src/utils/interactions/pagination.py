from typing import (
    Final, 
    Dict, 
    Any,
    List,
    Optional,
)


DEFAULT_PAGINATION_LIMIT: Final[int] = 10


class Pagination:

    def __init__(self, data: List[Any], text: str) -> None:
        self.data = data
        self.text = text
        self._page = 0
        self._limit = DEFAULT_PAGINATION_LIMIT

    def is_next_data_exists(self) -> bool:

        end = self._page + 10
        next_data = self.data[self._page:end]
        
        if not next_data:
            return False
        
        return True
    
    def is_previous_data_exists(self) -> bool:

        start = self._page - 20 if (self._page - 20) > 0 else 0
        end = self._page - 10
        previous_data = self.data[start:end]
        
        if not previous_data:
            return False
        
        return True
        

    def next(self) -> List[Any]:
        
        end = self._page + 10
        next_data = self.data[self._page:end]
        
        if not next_data:
            return []
        
        self._page = end

        return next_data

    def previous(self) -> List[Any]:
        
        start = self._page - 20 if (self._page - 20) > 0 else 0
        end = self._page - 10
        previous_data = self.data[start:end]
        
        if not previous_data:
            return []
        
        self._page = end
        return previous_data


class PaginationMediator:

    def __init__(self) -> None:
        self.data: Dict[int, Pagination] = {}

    def add(self, user_id: int, data: List[Any], text: str) -> None:
        self.data[user_id] = Pagination(data, text)
    
    def get(self, user_id: int) -> Optional[Pagination]:
        return self.data.get(user_id)
    
    def clear(self, user_id: int) -> None:
        self.data.pop(user_id, None)
        