"""
conftest module for pytest fixtures.

This module contains fixtures used by pytest to set up the test environment.

Usage:
    pytest automatically detects and uses the fixtures defined in this file.
"""
import asyncio
from typing import Dict, List

import httpx
import pytest

from app.database.db import reset_dbs
from app.main import app
from app.models.products import ProductIn
from app.models.reviews import ReviewIn
from app.security.jwt import create_token


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
async def username() -> str:
    return "martin.muller@google.com"


@pytest.fixture(scope="session")
def access_token(username) -> str:
    return create_token(username)


@pytest.fixture(scope="session")
def auth_headers(access_token) -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }


@pytest.fixture(scope="session")
def auth_headers_no_token() -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer ",
    }


@pytest.fixture(scope="session")
def good_user(username) -> Dict[str, str]:
    return {
        "email": username,
        "password": "test_password",
    }


@pytest.fixture(scope="session")
def good_user_auth(username) -> Dict[str, str]:
    return {
        "username": username,
        "password": "test_password",
    }


@pytest.fixture(scope="session")
def headers() -> Dict[str, str]:
    return {"accept": "application/json", "Content-Type": "application/json"}


@pytest.fixture(scope="session")
def form_headers() -> Dict[str, str]:
    return {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }


@pytest.fixture(scope="session")
def mock_products() -> List[ProductIn]:
    new_product1 = ProductIn(
        name="Fairphone 4",
        category="smartphone",
        score="90",
    )
    new_product2 = ProductIn(
        name="iPhone 14",
        category="smartphone",
        score="75",
    )
    return [new_product1, new_product2]


@pytest.fixture(scope="session")
def mock_reviews() -> List[ReviewIn]:
    new_review1 = ReviewIn(
        content="I really like this product",
    )
    new_review2 = ReviewIn(
        content="I don't really like this product",
    )
    new_review3 = ReviewIn(
        content="I love this product",
    )
    return [new_review1, new_review2, new_review3]


@pytest.fixture(scope="module", autouse=True)
def reset_databases():
    reset_dbs()
