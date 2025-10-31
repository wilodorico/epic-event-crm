from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.event.event_repository_abc import EventRepositoryABC


class GetUnassignedEventsUseCase(UseCaseABC):
    """Handles the retrieval of all events without an assigned support contact.

    This use case ensures that only authorized collaborators can view the list of unassigned events.
    It returns all event records that do not have a support contact assigned yet.

    Requires the FILTER_EVENTS permission to execute.
    """

    permissions = Permissions.FILTER_EVENTS

    def __init__(self, auth_context: AuthContextABC, event_repository: EventRepositoryABC):
        super().__init__(auth_context)
        self._event_repository = event_repository

    def _execute(self):
        """Retrieves and returns all unassigned event entities.

        Args:
            None

        Raises:
            PermissionError: If the user lacks permissions.

        Returns:
            list[Event]: A list of event entities without an assigned support contact.
        """
        return self._event_repository.get_all_unassigned()
