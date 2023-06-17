from threading import Lock
from typing import Any, Dict, List


class Database:
    def __init__(self, model: Any, collection: Dict[int, Any] = dict()) -> None:
        self.index: int = 0
        self.collection: Dict[int, Any] = collection
        self.model: Any = model
        self.Lock: Lock = Lock()

    def _insert_index(self, data: Any, index: int) -> Any:
        new_data = self.model(**data.dict(), id=index)
        return new_data

    async def get(self, index: int) -> Any:
        with self.Lock:
            return self.collection.get(index)

    async def get_all(self) -> List[Any]:
        with self.Lock:
            return list(self.collection.values())

    async def delete(self, index: int) -> Any:
        with self.Lock:
            return self.collection.pop(index, None)

    async def save(self, data: Any) -> Any:
        with self.Lock:
            new_data = self._insert_index(data, self.index)
            self.collection[self.index] = new_data
            self.index += 1
            return new_data

    async def update(self, id: int, data: Any):
        with self.Lock:
            data.id = id
            self.collection[id] = data
