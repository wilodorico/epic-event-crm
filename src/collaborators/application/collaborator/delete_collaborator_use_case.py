from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.collaborator_repository_abc import CollaboratorRepositoryABC
from collaborators.domain.collaborator.permissions import Permissions
from commons.id_generator_abc import IdGeneratorABC


class DeleteCollaboratorUseCase:
    def __init__(
        self, repository: CollaboratorRepositoryABC, id_generator: IdGeneratorABC, auth_context: AuthContextABC
    ):
        self._repository = repository
        self._id_generator = id_generator
        self._auth_context = auth_context

    def execute(self, requester: Collaborator, collaborator_id: str) -> None:
        self._auth_context.ensure(Permissions.DELETE_COLLABORATOR)

        collaborator = self._repository.find_by_id(collaborator_id)
        if not collaborator:
            raise ValueError("Collaborator not found.")

        self._repository.delete(collaborator.id)
