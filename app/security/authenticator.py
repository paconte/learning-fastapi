from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.security.jwt import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")


async def authenticate(token: str = Depends(oauth2_scheme)) -> str:
    """
    Authenticates the user based on the provided JSON Web Token (JWT).

    Args:
        token (str): The JWT token.

    Returns:
        str: The user identifier.

    Raises:
        HTTPException: If the token is invalid or has expired.
    """
    decoded_token = await verify_token(token)
    return decoded_token["user"]
