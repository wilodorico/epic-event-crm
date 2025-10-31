from collaborators.application.exceptions.authorization_error import AuthorizationError
from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.domain.collaborator.permissions import Permissions


class AuthContext(AuthContextABC):
    """Concrete implementation of authorization context using role-based permissions.

    This class manages user authorization by mapping each role (Management, Commercial, Support)
    to its set of allowed permissions. It validates operations against the current user's role
    and raises authorization errors when permissions are insufficient.
    """

    _permissions = {
        Role.MANAGEMENT: {
            Permissions.CREATE_COLLABORATOR,
            Permissions.UPDATE_COLLABORATOR,
            Permissions.DELETE_COLLABORATOR,
            Permissions.CREATE_CONTRACT,
            Permissions.UPDATE_CONTRACT,
            Permissions.READ_CUSTOMERS,
            Permissions.READ_CONTRACTS,
            Permissions.SIGN_CONTRACT,
            Permissions.READ_EVENTS,
            Permissions.FILTER_EVENTS,
            Permissions.ASSIGN_EVENT,
        },
        Role.COMMERCIAL: {
            Permissions.CREATE_CUSTOMER,
            Permissions.UPDATE_CUSTOMER,
            Permissions.UPDATE_CONTRACT,
            Permissions.READ_CUSTOMERS,
            Permissions.READ_CONTRACTS,
            Permissions.SIGN_CONTRACT,
            Permissions.CREATE_EVENT,
            Permissions.READ_EVENTS,
            Permissions.FILTER_CONTRACTS,
        },
        Role.SUPPORT: {
            Permissions.READ_CUSTOMERS,
            Permissions.READ_CONTRACTS,
            Permissions.READ_EVENTS,
            Permissions.UPDATE_EVENT,
        },
    }

    def __init__(self, user: Collaborator):
        """Initializes the authorization context for a specific user.

        Args:
            user: The collaborator whose permissions will be checked.
        """
        self.user = user

    def can(self, permission: Permissions) -> bool:
        """Checks if the current user has the specified permission based on their role.

        Args:
            permission: The permission to check.

        Returns:
            bool: True if the user's role includes the permission, False otherwise.
        """
        allowed = self._permissions.get(self.user.role, set())
        return permission in allowed

    def ensure(self, permission: Permissions) -> None:
        """Ensures the current user has the specified permission, raising an error if not.

        Args:
            permission: The permission to enforce.

        Raises:
            AuthorizationError: If the user's role does not include the permission.

        Returns:
            None
        """
        if not self.can(permission):
            raise AuthorizationError(self.user, permission)
