from pydantic import BaseModel


class ReviewBase(BaseModel):
    content: str
    user_id: int


class Review(ReviewBase):
    id: int


class ReviewIn(ReviewBase):
    pass
