from collaborators.application.exceptions.authorization_error import AuthorizationError
from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.domain.collaborator.permissions import Permissions


class AuthContext(AuthContextABC):
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
        self.user = user

    def can(self, permission: Permissions) -> bool:
        allowed = self._permissions.get(self.user.role, set())
        return permission in allowed

    def ensure(self, permission: Permissions) -> None:
        if not self.can(permission):
            raise AuthorizationError(self.user, permission)
