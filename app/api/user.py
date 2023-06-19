# User endpoints

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.database.db import USER_DB
from app.models.users import User, UserToken
from app.security.hash import Hasher
from app.security.jwt import create_token

user_router = APIRouter()
hasher = Hasher()


@user_router.post("/user/signup", summary="Create a new user")
async def sign_up(user: User) -> dict:
    """
    Create a new user.

    Args:
        user (User): The user information.

    Returns:
        dict: A message indicating the successful creation of the user.

    Raises:
        HTTPException: If the user with the supplied email already exists.
    """
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


@user_router.post(
    "/user/signin", response_model=UserToken, summary="User authentication"
)
async def sign_in(form: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Authenticate a user and generate an access token.

    Args:
        form (OAuth2PasswordRequestForm): The form data containing
            the user credentials.

    Returns:
        dict: The access token and token type.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    user_passwd = USER_DB.get(form.username)
    if not user_passwd:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )
    if hasher.verify(form.password, user_passwd):
        access_token = create_token(form.username)
        return {"access_token": access_token, "token_type": "Bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials.",
    )
