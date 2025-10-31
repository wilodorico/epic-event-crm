from abc import ABC, abstractmethod


class PasswordHasherABC(ABC):
    """Abstract base class defining the interface for password hashing services."""

    @abstractmethod
    def hash(self, plain_password: str) -> str:
        """Hash the given password and return the hashed value."""
        pass

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify that the given password matches the hashed value."""
        pass
