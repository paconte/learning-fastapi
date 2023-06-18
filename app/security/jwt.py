import secrets
import time
from datetime import datetime
from typing import Dict

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.models.users import User

generated_key = secrets.token_urlsafe(nbytes=32)


def create_token(user: str) -> str:
    payload = {"user": user, "expires": time.time() + 3600}
    token = jwt.encode(payload, generated_key, algorithm="HS256")
    return token


def verify_token(token: str, user_db: Dict[int, User]) -> dict:
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

        user_exist = user_db.get(data["user"])
        if not user_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
            )

        return data

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )
