from pydantic import BaseModel, EmailStr


class ReviewBase(BaseModel):
    content: str


class Review(ReviewBase):
    user: EmailStr


class ReviewIn(ReviewBase):
    pass
