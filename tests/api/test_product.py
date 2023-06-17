from typing import Dict, List

import httpx
import pytest

from app.database import Database
from app.models.products import Product, ProductIn


@pytest.fixture(scope="module")
def collection() -> Dict[int, Product]:
    return dict()


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
async def mock_db(
    collection: Dict[int, Product], mock_products: List[ProductIn]
) -> Database:
    db = Database(Product, collection)
    for product in mock_products:
        await db.save(product)
    return db


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
    print(response.json())
    for i, product in enumerate(mock_products):
        url = f"/products/{str(i)}"
        product.score = "89"
        print(product.dict())
        response = await client.put(url, json=product.dict())
        assert response.status_code == 200
        assert response.json()["id"] == i
        assert response.json()["name"] == product.name
        assert response.json()["category"] == product.category
        assert response.json()["score"] == "89"


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
