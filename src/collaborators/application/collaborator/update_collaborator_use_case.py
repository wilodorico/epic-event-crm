from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.collaborator_repository_abc import CollaboratorRepositoryABC
from collaborators.domain.collaborator.permissions import Permissions


class UpdateCollaboratorUseCase:
    def __init__(self, repository: CollaboratorRepositoryABC, auth_context: AuthContextABC):
        self._repository = repository
        self._auth_context = auth_context

    def execute(self, updater: Collaborator, collaborator_id: str, data: dict) -> Collaborator:
        self._auth_context.ensure(Permissions.UPDATE_COLLABORATOR)

        collaborator = self._repository.find_by_id(collaborator_id)
        if not collaborator:
            raise ValueError("Collaborator not found.")

        collaborator.update(data, updater.id)
        self._repository.update(collaborator)

        return collaborator
