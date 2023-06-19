from threading import Lock
from typing import Any, Dict, List

from app.models.products import Product
from app.models.reviews import Review


class Database:
    def __init__(self, model: Any) -> None:
        """
        Initializes the Database instance.

        Args:
            model (Any): The model class representing the data structure.

        Attributes:
            index (int): The index counter for assigning IDs to data.
            collection (Dict[int, Any]): The collection of data items.
            model (Any): The model class representing the data structure.
            lock (Lock): The lock object for thread safety.
        """
        self.index: int = 0
        self.collection: Dict[int, Any] = dict()
        self.model: Any = model
        self.lock: Lock = Lock()

    def _insert_id_and_review(self, data: Any, index: int) -> Any:
        """
        Inserts the ID and an empty list of reviews into the data object.

        Args:
            data (Any): The data object to insert the ID and reviews.
            index (int): The ID value to be assigned.

        Returns:
            Any: The modified data object with the ID and reviews.

        Raises:
            ValueError: If the ID in the data object does not match the key ID.
        """
        new_data = self.model(**data.dict(), id=index, reviews=[])
        return new_data

    async def get(self, index: int) -> Any:
        """
        Retrieves a data item by its ID.

        Args:
            index (int): The ID of the data item to retrieve.

        Returns:
            Any: The data item with the specified ID, or None if not found.
        """
        with self.lock:
            return self.collection.get(index)

    async def get_all(self) -> List[Any]:
        """
        Retrieves all data items in the collection.

        Returns:
            List[Any]: A list of all data items in the collection.
        """
        with self.lock:
            return list(self.collection.values())

    async def delete(self, index: int) -> Any:
        """
        Deletes a data item from the collection.

        Args:
            index (int): The ID of the data item to delete.

        Returns:
            Any: The deleted data item, or None if not found.
        """
        with self.lock:
            return self.collection.pop(index, None)

    async def save(self, data: Any) -> Any:
        """
        Saves a new data item to the collection.

        Args:
            data (Any): The data item to save.

        Returns:
            Any: The saved data item with the assigned ID.

        Raises:
            ValueError: If the ID in the data item does not match the key ID.
        """
        with self.lock:
            new_data = self._insert_id_and_review(data, self.index)
            self.collection[self.index] = new_data
            self.index += 1
            return new_data

    async def update(self, id: int, data: Any) -> Any:
        """
        Updates a data item in the collection.

        Args:
            id (int): The ID of the data item to update.
            data (Any): The updated data item.

        Returns:
            Any: The updated data item, or None if not found.

        Raises:
            ValueError: If the ID in the data item does not match the key ID.
        """
        with self.lock:
            if isinstance(data, self.model):
                if data.id != id:
                    raise ValueError("ID in data does not match key ID")
                new_data = data
            else:
                new_data = self._insert_id_and_review(data, id)
            if id in self.collection:
                self.collection[id] = new_data
                return new_data

    def reset(self) -> None:
        with self.lock:
            self.collection.clear()
            self.index = 0


PRODUCT_DB: Database = Database(Product)
REVIEW_DB: Database = Database(Review)
USER_DB: Dict[str, str] = dict()


def reset_dbs() -> None:
    PRODUCT_DB.reset()
    REVIEW_DB.reset()
    USER_DB.clear()
