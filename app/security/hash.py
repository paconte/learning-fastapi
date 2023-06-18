from passlib.context import CryptContext

ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    def create(self, password: str) -> str:
        return ctx.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return ctx.verify(plain_password, hashed_password)
