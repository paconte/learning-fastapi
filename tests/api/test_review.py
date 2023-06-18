from typing import List

import httpx
import pytest

from app.api.product import product_db
from app.models.products import ProductIn
from app.models.reviews import ReviewIn


@pytest.mark.asyncio
async def test_empty_db(client: httpx.AsyncClient) -> None:
    response = await client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_post(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
) -> None:
    product_db.reset_index()
    for product in mock_products:
        response = await client.post("/products", json=product.dict())
        assert response.status_code == 200
        assert response.json() == {"message": "Product created successfully"}

    url = f"/products/{str(len(mock_products)-1)}/reviews"
    for review in mock_reviews:
        response = await client.post(url, json=review.dict())
        print(response.json())
        assert response.status_code == 200
        assert response.json() == {"message": "Review created successfully"}


async def test_get_all_product_reviews(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
) -> None:
    url = f"/products/{str(len(mock_products)-1)}/reviews"
    response = await client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == len(mock_reviews)
    for i, review in enumerate(mock_reviews):
        assert response.json()[i]["id"] == i
        assert response.json()[i]["user_id"] == review.user_id
        assert response.json()[i]["content"] == review.content


async def test_get_single(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
) -> None:
    for i, review in enumerate(mock_reviews):
        url = f"/products/{str(len(mock_products)-1)}/reviews/{str(i)}"
        response = await client.get(url)
        assert response.status_code == 200
        assert response.json()["id"] == i
        assert response.json()["user_id"] == review.user_id
        assert response.json()["content"] == review.content


async def test_get_wrong(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
) -> None:
    url = (
        f"/products/{str(len(mock_products)-1)}"
        f"/reviews/{str(len(mock_reviews) + 1)}"
    )
    response = await client.get(url)
    assert response.status_code == 404


async def test_update(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
) -> None:
    for i, _ in enumerate(mock_reviews):
        url = f"/products/{str(len(mock_products)-1)}/reviews/{str(i)}"
        new_review = mock_reviews[i]
        new_review.content = "Best product ever"
        response = await client.put(url, json=new_review.dict())
        assert response.status_code == 200
        assert response.json()["user_id"] == new_review.user_id
        assert response.json()["content"] == new_review.content


async def test_update_wrong(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
) -> None:
    url = (
        f"/products/{str(len(mock_products)-1)}"
        f"/reviews/{str(len(mock_reviews) + 1)}"
    )
    new_review = mock_reviews[0]
    response = await client.put(url, json=new_review.dict())
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_review(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
) -> None:
    for i, _ in enumerate(mock_reviews):
        url = f"/products/{str(len(mock_products)-1)}/reviews/{str(i)}"
        response = await client.delete(url)
        assert response.status_code == 200
        assert response.json() == {"message": "Review deleted successfully"}
        response = await client.get(url)
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_wrong_product(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
) -> None:
    url = (
        f"/products/{str(len(mock_products)-1)}"
        f"/reviews/{str(len(mock_reviews) + 1)}"
    )
    response = await client.delete(url)
    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found"


@pytest.mark.asyncio
async def test_empty_reviews(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
) -> None:
    url = f"/products/{str(len(mock_products)-2)}/reviews"
    response = await client.get(url)
    assert response.status_code == 200
    assert response.json() == []
