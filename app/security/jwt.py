import secrets
import time
from datetime import datetime

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.database.db import USER_DB

generated_key = secrets.token_urlsafe(nbytes=32)


def create_token(user: str) -> str:
    payload = {"user": user, "expires": time.time() + 3600}
    token = jwt.encode(payload, generated_key, algorithm="HS256")
    return token


async def verify_token(token: str) -> dict:
    try:
        data = jwt.decode(token, generated_key, algorithms=["HS256"])
        expire = data.get("expires")

        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied",
            )
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token expired!"
            )

        user_exist = USER_DB.get(data["user"])
        if not user_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
            )

        return data

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )
