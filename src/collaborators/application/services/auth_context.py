from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.collaborator import Collaborator, Role


class AuthContext(AuthContextABC):
    def __init__(self, user: Collaborator):
        self.user = user

    def can_create_collaborator(self) -> bool:
        return self.user.role == Role.MANAGEMENT

    def ensure_can_create_collaborator(self) -> None:
        if not self.can_create_collaborator():
            raise PermissionError("Only managers can create collaborators")
