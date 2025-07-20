from abc import ABC, abstractmethod


class AuthContextABC(ABC):
    """Interface for managing permissions and authorizations."""

    @abstractmethod
    def can_create_collaborator(self) -> bool:
        """Checks if the collaborator can create another collaborator."""
        pass

    @abstractmethod
    def ensure_can_create_collaborator(self) -> None:
        """Ensures that the collaborator can create another collaborator, raises an exception otherwise."""
        pass
