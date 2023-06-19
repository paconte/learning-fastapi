# User endpoints

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.database.db import USER_DB
from app.models.users import User, UserToken
from app.security.hash import Hasher
from app.security.jwt import create_token

user_router = APIRouter()
hasher = Hasher()


@user_router.post("/user/signup")
async def sign_up(user: User) -> dict:
    user_passwd = USER_DB.get(user.email)
    if user_passwd:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User exists already.",
        )
    hashed_password = hasher.create(user.password)
    user.password = hashed_password
    USER_DB[user.email] = user.password
    return {"message": "User created successfully"}


@user_router.post("/user/signin", response_model=UserToken)
async def sign_in(form: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_passwd = USER_DB.get(form.username)
    if not user_passwd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrong credentials.",
        )
    if hasher.verify(form.password, user_passwd):
        access_token = create_token(form.username)
        return {"access_token": access_token, "token_type": "Bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed.",
    )
