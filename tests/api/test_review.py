from typing import Dict, List

import httpx
import pytest

from app.models.products import ProductIn
from app.models.reviews import ReviewIn


@pytest.mark.asyncio
async def test_empty_db(client: httpx.AsyncClient) -> None:
    response = await client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_and_login_user(
    client: httpx.AsyncClient,
    good_user: Dict[str, str],
    good_user_auth: Dict[str, str],
    form_headers: Dict[str, str],
    headers: Dict[str, str],
) -> None:
    # Create user
    response = await client.post(
        "/user/signup", json=good_user, headers=headers
    )
    assert response.status_code == 200
    # Login user
    response = await client.post(
        "/user/signin", data=good_user_auth, headers=form_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_post(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
    auth_headers: Dict[str, str],
) -> None:
    # Create products
    for product in mock_products:
        response = await client.post(
            "/products",
            json=product.dict(),
            headers=auth_headers,
        )
        print(response.json())
        assert response.status_code == 200
        assert response.json()["message"] == "Product created successfully"

    # Create reviews
    url = f"/products/{str(len(mock_products)-1)}/reviews"
    for review in mock_reviews:
        response = await client.post(
            url, json=review.dict(), headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Review created successfully"}


@pytest.mark.asyncio
async def test_create_for_non_existant_product(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
    auth_headers: Dict[str, str],
) -> None:
    url = f"/products/{str(len(mock_products)+1)}/reviews"

    for review in mock_reviews:
        response = await client.post(
            url, json=review.dict(), headers=auth_headers
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Product not found"}


@pytest.mark.asyncio
async def test_get_all_product_reviews(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
    username: str,
) -> None:
    url = f"/products/{str(len(mock_products)-1)}/reviews"
    response = await client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == len(mock_reviews)
    for i, review in enumerate(mock_reviews):
        assert response.json()[i]["user"] == username
        assert response.json()[i]["content"] == review.content


@pytest.mark.asyncio
async def test_empty_product_reviews(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
) -> None:
    url = f"/products/{str(len(mock_products)-2)}/reviews"
    response = await client.get(url)

    assert response.status_code == 200
    assert response.json() == []


"""
@pytest.mark.skip
@pytest.mark.asyncio
async def test_get_single_review(
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


@pytest.mark.skip
@pytest.mark.asyncio
async def test_get_non_existent_review(
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


@pytest.mark.skip
@pytest.mark.asyncio
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


@pytest.mark.skip
@pytest.mark.asyncio
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


@pytest.mark.skip
@pytest.mark.asyncio
async def test_update_from_wrong_product(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
) -> None:
    url = f"/products/{str(len(mock_products)+1)}/reviews/0"
    new_review = mock_reviews[0]
    response = await client.put(url, json=new_review.dict())
    assert response.status_code == 404


@pytest.mark.skip
@pytest.mark.asyncio
async def test_delete_review(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
    auth_headers: Dict[str, str],
) -> None:
    for i, _ in enumerate(mock_reviews):
        url = f"/products/{str(len(mock_products)-1)}/reviews/{str(i)}"
        response = await client.delete(url, headers=auth_headers)

        assert response.status_code == 200
        assert response.json() == {"message": "Review deleted successfully"}

        response = await client.get(url)
        assert response.status_code == 404


@pytest.mark.skip
@pytest.mark.asyncio
async def test_delete_non_existant_review(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    mock_reviews: List[ReviewIn],
    auth_headers: Dict[str, str],
) -> None:
    url = (
        f"/products/{str(len(mock_products)-1)}"
        f"/reviews/{str(len(mock_reviews) + 1)}"
    )
    response = await client.delete(url, headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found"


@pytest.mark.skip
@pytest.mark.asyncio
async def test_delete_non_existant_product(
    client: httpx.AsyncClient,
    mock_products: List[ProductIn],
    auth_headers: Dict[str, str],
) -> None:
    url = f"/products/{str(len(mock_products)+1)}/reviews/0"
    response = await client.delete(url, headers=auth_headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"
"""
