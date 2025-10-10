from collaborators.application.services.password_hasher_abc import PasswordHasherABC


class FakePasswordHasher(PasswordHasherABC):
    def hash(self, plain_password: str) -> str:
        return f"hashed-{plain_password}"

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return hashed_password == f"hashed-{plain_password}"
