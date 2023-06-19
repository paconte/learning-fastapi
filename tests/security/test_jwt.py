import pytest
from fastapi import HTTPException, status
from freezegun import freeze_time

from app.database.db import USER_DB
from app.security.jwt import create_token, verify_token


def test_create_token():
    # Test that a token is created successfully
    user = "test_user"
    token = create_token(user)
    assert isinstance(token, str)


async def test_verify_token_valid():
    # Test that a valid token is verified successfully
    user = "test_user"
    token = create_token(user)
    USER_DB[user] = {"id": 1, "username": user}
    data = await verify_token(token)
    assert isinstance(data, dict)
    assert "user" in data
    assert data["user"] == user


async def test_verify_token_expired():
    # Test that an expired token raises an HTTPException with 403 status code
    user = "test_user"
    expired_token = create_token(user)
    USER_DB[user] = {"id": 1, "username": user}
    with pytest.raises(HTTPException) as exc_info:
        with freeze_time("5000-01-01"):
            await verify_token(expired_token)

    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN


async def test_verify_token_invalid():
    # Test that an invalid token raises an HTTPException with 400 status code
    invalid_token = "invalid_token"

    with pytest.raises(HTTPException) as exc_info:
        await verify_token(invalid_token)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


async def test_verify_token_no_user():
    # Test that a token from a deleted/unexistent user raises an
    # HTTPException with 400 status code
    user = "test_user"
    token = create_token(user)
    USER_DB.clear()
    with pytest.raises(HTTPException) as exc_info:
        await verify_token(token)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
