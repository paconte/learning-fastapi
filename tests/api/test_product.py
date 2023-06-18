from typing import List

import httpx
import pytest

from app.models.products import ProductIn


@pytest.mark.asyncio
async def test_empty_db(client: httpx.AsyncClient) -> None:
    response = await client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_post(
    client: httpx.AsyncClient, mock_products: List[ProductIn]
) -> None:
    for product in mock_products:
        response = await client.post("/products", json=product.dict())
        assert response.status_code == 200
        assert response.json() == {"message": "Product created successfully"}


@pytest.mark.asyncio
async def test_get_all(
    client: httpx.AsyncClient, mock_products: List[ProductIn]
) -> None:
    response = await client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == len(mock_products)
    for i, product in enumerate(mock_products):
        assert response.json()[i]["id"] == i
        assert response.json()[i]["name"] == product.name
        assert response.json()[i]["category"] == product.category
        assert response.json()[i]["score"] == product.score
        assert response.json()[i]["review_ids"] == product.review_ids


@pytest.mark.asyncio
async def test_get_single(
    client: httpx.AsyncClient, mock_products: List[ProductIn]
) -> None:
    for i, product in enumerate(mock_products):
        url = f"/products/{str(i)}"
        response = await client.get(url)
        assert response.status_code == 200
        assert response.json()["id"] == i
        assert response.json()["name"] == product.name
        assert response.json()["category"] == product.category
        assert response.json()["score"] == product.score
        assert response.json()["review_ids"] == product.review_ids


@pytest.mark.asyncio
async def test_get_wrong(
    client: httpx.AsyncClient, mock_products: List[ProductIn]
) -> None:
    url = f"/products/{str(len(mock_products) + 1)}"
    response = await client.get(url)
    assert response.status_code == 404
    assert (
        response.json()["detail"] == "Product with supplied ID does not exist"
    )


@pytest.mark.asyncio
async def test_update(
    client: httpx.AsyncClient, mock_products: List[ProductIn]
) -> None:
    response = await client.get("/products")
    for i, product in enumerate(mock_products):
        url = f"/products/{str(i)}"
        product.score = "89"
        response = await client.put(url, json=product.dict())
        assert response.status_code == 200
        assert response.json()["id"] == i
        assert response.json()["name"] == product.name
        assert response.json()["category"] == product.category
        assert response.json()["score"] == "89"
        assert response.json()["review_ids"] == product.review_ids


async def test_update_wrong(
    client: httpx.AsyncClient, mock_products: List[ProductIn]
) -> None:
    url = f"/products/{str(len(mock_products) + 1)}"
    product = mock_products[0]
    response = await client.put(url, json=product.dict())
    assert response.status_code == 404
    assert (
        response.json()["detail"] == "Product with supplied ID does not exist"
    )


@pytest.mark.asyncio
async def test_delete_product(
    client: httpx.AsyncClient, mock_products: List[ProductIn]
) -> None:
    for i, _ in enumerate(mock_products):
        url = f"/products/{str(i)}"
        response = await client.delete(url)
        assert response.status_code == 200
        assert response.json() == {"message": "Product deleted successfully."}
        response = await client.get(url)
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_wrong_product(
    client: httpx.AsyncClient, mock_products: List[ProductIn]
) -> None:
    url = f"/products/{str(len(mock_products) + 1)}"
    response = await client.delete(url)
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


@pytest.mark.asyncio
async def test_db_empty_again(client: httpx.AsyncClient) -> None:
    response = await client.get("/products")
    assert response.status_code == 200
    assert response.json() == []
