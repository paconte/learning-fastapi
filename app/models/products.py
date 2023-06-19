from typing import List

from pydantic import BaseModel

from app.models.reviews import Review


class ProductBase(BaseModel):
    name: str
    category: str
    score: str


class Product(ProductBase):
    id: int
    reviews: List[Review]


class ProductIn(ProductBase):
    pass
