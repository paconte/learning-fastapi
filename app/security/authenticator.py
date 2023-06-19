from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.security.jwt import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")


async def authenticate(token: str = Depends(oauth2_scheme)) -> str:
    decoded_token = await verify_token(token)
    return decoded_token["user"]
