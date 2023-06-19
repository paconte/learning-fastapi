from passlib.context import CryptContext

ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """
    Helper class for password hashing and verification.
    """

    def create(self, password: str) -> str:
        """
        Hashes the given password.

        Args:
            password (str): The plain password.

        Returns:
            str: The hashed password.
        """
        return ctx.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifies if the plain password matches the hashed password.

        Args:
            plain_password (str): The plain password.
            hashed_password (str): The hashed password.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return ctx.verify(plain_password, hashed_password)
