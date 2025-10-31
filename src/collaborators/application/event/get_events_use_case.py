from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.event.event_repository_abc import EventRepositoryABC


class GetEventsUseCase(UseCaseABC):
    """Handles the retrieval of all events in the system.

    This use case ensures that only authorized collaborators can view the complete list
    of events and returns all event records from the repository.

    Requires the READ_EVENTS permission to execute.
    """

    permissions = Permissions.READ_EVENTS

    def __init__(self, auth_context: AuthContextABC, event_repository: EventRepositoryABC):
        super().__init__(auth_context)
        self._event_repository = event_repository

    def _execute(self):
        """Retrieves and returns all event entities.

        Args:
            None

        Raises:
            PermissionError: If the user lacks permissions.

        Returns:
            list[Event]: A list of all event entities in the system.
        """
        return self._event_repository.get_all()
