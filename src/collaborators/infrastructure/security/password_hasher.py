import bcrypt

from collaborators.application.services.password_hasher_abc import PasswordHasherABC


class BcryptPasswordHasher(PasswordHasherABC):
    """Concrete implementation of password hashing using bcrypt."""

    def hash(self, plain_password: str) -> str:
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
