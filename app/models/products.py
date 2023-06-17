from typing import List

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    category: str
    score: str
    review_ids: List[int]


class Product(ProductBase):
    id: int


class ProductIn(ProductBase):
    pass
