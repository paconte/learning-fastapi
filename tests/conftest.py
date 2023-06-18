import asyncio
from typing import List

import httpx
import pytest

from app.main import app
from app.models.products import ProductIn
from app.models.reviews import ReviewIn


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="module")
def mock_products() -> List[ProductIn]:
    new_product1 = ProductIn(
        name="Fairphone 4",
        category="smartphone",
        score="90",
        review_ids=[],
    )
    new_product2 = ProductIn(
        name="iPhone 14",
        category="smartphone",
        score="75",
        review_ids=[],
    )
    return [new_product1, new_product2]


@pytest.fixture(scope="module")
def mock_reviews() -> List[ReviewIn]:
    new_review1 = ReviewIn(
        user_id=1,
        content="I really like this product",
    )
    new_review2 = ReviewIn(
        user_id=2,
        content="I don't really like this product",
    )
    new_review3 = ReviewIn(
        user_id=3,
        content="I love this product",
    )
    return [new_review1, new_review2, new_review3]
