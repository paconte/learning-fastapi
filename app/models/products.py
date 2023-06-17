from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    category: str
    score: str


class Product(ProductBase):
    id: int


class ProductIn(ProductBase):
    pass
