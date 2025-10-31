from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.event.event_repository_abc import EventRepositoryABC


class GetSupportEventsUseCase(UseCaseABC):
    """Handles the retrieval of all events assigned to a specific support contact.

    This use case ensures that only authorized collaborators can view events filtered by
    support contact and returns all event records assigned to the specified support.

    Requires the READ_EVENTS permission to execute.
    """

    permissions = Permissions.READ_EVENTS

    def __init__(self, auth_context: AuthContextABC, event_repository: EventRepositoryABC):
        super().__init__(auth_context)
        self._event_repository = event_repository

    def _execute(self, support_id):
        """Retrieves and returns all events assigned to a support contact.

        Args:
            support_id: The unique identifier of the support contact.

        Raises:
            PermissionError: If the user lacks permissions.

        Returns:
            list[Event]: A list of event entities assigned to the specified support contact.
        """
        return self._event_repository.get_by_support_id(support_id)
