from threading import Lock
from typing import Any, Dict, List


class Database:
    def __init__(self, model: Any) -> None:
        self.index: int = 0
        self.collection: Dict[int, Any] = dict()
        self.model: Any = model
        self.lock: Lock = Lock()

    def _insert_index(self, data: Any, index: int) -> Any:
        new_data = self.model(**data.dict(), id=index)
        return new_data

    async def get(self, index: int) -> Any:
        with self.lock:
            return self.collection.get(index)

    async def get_all(self) -> List[Any]:
        with self.lock:
            return list(self.collection.values())

    async def delete(self, index: int) -> Any:
        with self.lock:
            return self.collection.pop(index, None)

    async def save(self, data: Any) -> Any:
        with self.lock:
            new_data = self._insert_index(data, self.index)
            self.collection[self.index] = new_data
            self.index += 1
            return new_data

    async def update(self, id: int, data: Any) -> Any:
        with self.lock:
            if isinstance(data, self.model):
                if data.id != id:
                    raise ValueError("ID in data does not match key ID")
                new_data = data
            else:
                new_data = self._insert_index(data, id)
            if id in self.collection:
                self.collection[id] = new_data
                return new_data

    def reset_index(self) -> None:
        with self.lock:
            self.index = 0
