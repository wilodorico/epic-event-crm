from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.collaborator_repository_abc import CollaboratorRepositoryABC
from collaborators.domain.collaborator.permissions import Permissions


class UpdateCollaboratorUseCase(UseCaseABC):
    """Handles the update of a collaborator's information by a manager.

    This use case ensures that only authorized managers can update collaborator data.
    It validates the existence of the collaborator, applies the provided changes,
    and persists the updated record in the repository.
    """

    permissions = Permissions.UPDATE_COLLABORATOR

    def __init__(self, auth_context: AuthContextABC, repository: CollaboratorRepositoryABC):
        super().__init__(auth_context)
        self._repository = repository

    def _execute(self, updater: Collaborator, collaborator_id: str, data: dict) -> Collaborator:
        """Updates a collaborator's information.

        Args:
            updater: The collaborator performing the update (usually a manager).
            collaborator_id: The unique identifier of the collaborator to update.
            data: Dictionary containing the fields to update and their new values.

        Raises:
            ValueError: If the collaborator is not found.
            PermissionError: If the updater lacks permissions.

        Returns:
            The updated collaborator with the new information persisted in the repository.
        """
        collaborator = self._repository.find_by_id(collaborator_id)
        if not collaborator:
            raise ValueError("Collaborator not found.")

        collaborator.update(data, updater.id)
        self._repository.update(collaborator)

        return collaborator
