from abc import ABC, abstractmethod

from collaborators.domain.collaborator.permissions import Permissions


class AuthContextABC(ABC):
    """Abstract base class for authorization context management.

    This interface defines the contract for checking and enforcing user permissions
    within the application. Implementations should determine whether a user has the
    required permission to perform specific operations.
    """

    @abstractmethod
    def can(self, permission: Permissions) -> bool:
        """Checks if the current user has the specified permission.

        Args:
            permission: The permission to check.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        ...

    @abstractmethod
    def ensure(self, permission: Permissions) -> None:
        """Ensures the current user has the specified permission.

        Args:
            permission: The permission to enforce.

        Raises:
            AuthorizationError: If the user lacks the required permission.

        Returns:
            None
        """
        ...
