from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.domain.collaborator.permissions import Permissions


class AuthContext(AuthContextABC):
    _permissions = {
        Role.MANAGEMENT: {
            Permissions.CREATE_COLLABORATOR,
            Permissions.UPDATE_COLLABORATOR,
            Permissions.DELETE_COLLABORATOR,
        },
        Role.COMMERCIAL: {Permissions.CREATE_CUSTOMER},
    }

    def __init__(self, user: Collaborator):
        self.user = user

    def can(self, permission: Permissions) -> bool:
        allowed = self._permissions.get(self.user.role, set())
        return permission in allowed

    def ensure(self, permission: Permissions) -> None:
        if not self.can(permission):
            raise PermissionError("You do not have permission to perform this action.")
