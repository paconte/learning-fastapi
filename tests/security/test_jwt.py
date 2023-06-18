import pytest
from fastapi import HTTPException, status
from freezegun import freeze_time

from app.security.jwt import create_token, verify_token


def test_create_token():
    # Test that a token is created successfully
    user = "test_user"
    token = create_token(user)
    assert isinstance(token, str)


def test_verify_token_valid():
    # Test that a valid token is verified successfully
    user = "test_user"
    token = create_token(user)
    user_db = {user: {"id": 1, "username": user}}
    data = verify_token(token, user_db)
    assert isinstance(data, dict)
    assert "user" in data
    assert data["user"] == user


def test_verify_token_expired():
    # Test that an expired token raises an HTTPException with 403 status code
    user = "test_user"
    expired_token = create_token(user)
    user_db = {user: {"id": 1, "username": user}}
    with pytest.raises(HTTPException) as exc_info:
        with freeze_time("5000-01-01"):
            verify_token(expired_token, user_db)

    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN


def test_verify_token_invalid():
    # Test that an invalid token raises an HTTPException with 400 status code
    user = "test_user"
    invalid_token = "invalid_token"
    user_db = {user: {"id": 1, "username": user}}

    with pytest.raises(HTTPException) as exc_info:
        verify_token(invalid_token, user_db)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
