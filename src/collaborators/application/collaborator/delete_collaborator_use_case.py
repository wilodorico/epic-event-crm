from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator_repository_abc import CollaboratorRepositoryABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.sentry_config import capture_message
from commons.id_generator_abc import IdGeneratorABC


class DeleteCollaboratorUseCase(UseCaseABC):
    """Handles the deletion of a collaborator by a manager.

    This use case ensures that only authorized managers can delete collaborators.
    It validates the existence of the collaborator and permanently removes the record
    from the repository.
    """

    permissions = Permissions.DELETE_COLLABORATOR

    def __init__(
        self, auth_context: AuthContextABC, repository: CollaboratorRepositoryABC, id_generator: IdGeneratorABC
    ):
        super().__init__(auth_context)
        self._repository = repository
        self._id_generator = id_generator

    def _execute(self, collaborator_id: str) -> None:
        """Deletes a collaborator.

        Args:
            collaborator_id: The unique identifier of the collaborator to delete.

        Raises:
            ValueError: If the collaborator is not found.
            PermissionError: If the deleter lacks permissions.

        Returns:
            None. The collaborator is permanently removed from the repository.
        """
        collaborator = self._repository.find_by_id(collaborator_id)
        if not collaborator:
            raise ValueError("Collaborator not found.")

        # Capture collaborator info before deletion for logging
        collaborator_email = collaborator.email
        collaborator_role = collaborator.role.value

        self._repository.delete(collaborator.id)

        # Log collaborator deletion to Sentry
        capture_message(
            f"Collaborator deleted: {collaborator_email}",
            level="warning",
            collaborator_id=collaborator_id,
            collaborator_email=collaborator_email,
            collaborator_role=collaborator_role,
            deleted_by=self._auth_context.user.id if hasattr(self._auth_context, "user") else None,
        )
