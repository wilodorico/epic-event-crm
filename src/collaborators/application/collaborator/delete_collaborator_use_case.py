from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.collaborator_repository_abc import CollaboratorRepositoryABC
from collaborators.domain.collaborator.permissions import Permissions
from commons.id_generator_abc import IdGeneratorABC


class DeleteCollaboratorUseCase(UseCaseABC):
    permissions = Permissions.DELETE_COLLABORATOR

    def __init__(
        self, auth_context: AuthContextABC, repository: CollaboratorRepositoryABC, id_generator: IdGeneratorABC
    ):
        super().__init__(auth_context)
        self._repository = repository
        self._id_generator = id_generator

    def _execute(self, requester: Collaborator, collaborator_id: str) -> None:
        collaborator = self._repository.find_by_id(collaborator_id)
        if not collaborator:
            raise ValueError("Collaborator not found.")

        self._repository.delete(collaborator.id)
