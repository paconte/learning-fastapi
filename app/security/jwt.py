import secrets
import time
from datetime import datetime

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.database.db import USER_DB

generated_key = secrets.token_urlsafe(nbytes=32)


def create_token(user: str) -> str:
    """
    Creates a JSON Web Token (JWT) for the specified user.

    Args:
        user (str): The user identifier.

    Returns:
        str: The generated JWT.
    """
    payload = {"user": user, "expires": time.time() + 3600}
    token = jwt.encode(payload, generated_key, algorithm="HS256")
    return token


async def verify_token(token: str) -> dict:
    """
    Verifies the authenticity of a JSON Web Token (JWT).

    Args:
        token (str): The JWT to be verified.

    Returns:
        dict: The decoded payload of the JWT.

    Raises:
        HTTPException: If the token is invalid or has expired.
    """
    try:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        data = jwt.decode(token, generated_key, algorithms=["HS256"])
        expire = data.get("expires")

        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired!",
            )

        user_exist = USER_DB.get(data["user"])
        if not user_exist:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        return data

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
