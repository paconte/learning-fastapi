from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    password: str


class UserToken(BaseModel):
    access_token: str
    token_type: str
