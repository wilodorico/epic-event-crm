from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.collaborator_repository_abc import CollaboratorRepositoryABC
from collaborators.domain.collaborator.permissions import Permissions


class UpdateCollaboratorUseCase(UseCaseABC):
    permissions = Permissions.UPDATE_COLLABORATOR

    def __init__(self, auth_context: AuthContextABC, repository: CollaboratorRepositoryABC):
        super().__init__(auth_context)
        self._repository = repository

    def _execute(self, updater: Collaborator, collaborator_id: str, data: dict) -> Collaborator:
        collaborator = self._repository.find_by_id(collaborator_id)
        if not collaborator:
            raise ValueError("Collaborator not found.")

        collaborator.update(data, updater.id)
        self._repository.update(collaborator)

        return collaborator
