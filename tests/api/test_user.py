from typing import Dict

import httpx
import pytest


@pytest.mark.asyncio
async def test_sign_up(
    client: httpx.AsyncClient,
    good_user: Dict[str, str],
    headers: Dict[str, str],
) -> None:
    response = await client.post(
        "/user/signup", json=good_user, headers=headers
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}


@pytest.mark.asyncio
async def test_double_sign_up(
    client: httpx.AsyncClient,
    good_user: Dict[str, str],
    headers: Dict[str, str],
) -> None:
    response = await client.post(
        "/user/signup", json=good_user, headers=headers
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "User exists already."


@pytest.mark.asyncio
async def test_sign_in(
    client: httpx.AsyncClient,
    good_user_auth: Dict[str, str],
    form_headers: Dict[str, str],
) -> None:
    response = await client.post(
        "/user/signin", data=good_user_auth, headers=form_headers
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_wrong_sign_in(
    client: httpx.AsyncClient,
    good_user_auth: Dict[str, str],
    form_headers: Dict[str, str],
) -> None:
    good_user_auth["password"] = "wrong_password"
    response = await client.post(
        "/user/signin", data=good_user_auth, headers=form_headers
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid details passed."
