from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.event.event_repository_abc import EventRepositoryABC


class AssignSupportToEventUseCase(UseCaseABC):
    """Handles the assignment of a support contact to an event by a manager.

    This use case ensures that only authorized managers can assign support contacts to events.
    It validates the event's existence, assigns the support contact, and saves the updated
    event record to the repository.

    Requires the ASSIGN_EVENT permission to execute.
    """

    permissions = Permissions.ASSIGN_EVENT

    def __init__(self, auth_context: AuthContextABC, event_repository: EventRepositoryABC):
        super().__init__(auth_context)
        self._event_repository = event_repository

    def _execute(self, collaborator: Collaborator, event_id: str, support_id: str):
        """Assigns a support contact to an event and persists the change.

        Args:
            collaborator: The collaborator performing the operation (usually a manager).
            event_id: The unique identifier of the event to assign.
            support_id: The unique identifier of the support contact to assign.

        Raises:
            ValueError: If the event is not found.
            PermissionError: If the user lacks permissions.

        Returns:
            Event: The updated event entity with the assigned support contact.
        """
        event = self._event_repository.find_by_id(event_id)

        if not event:
            raise ValueError("Event not found.")

        event.assign_support(collaborator.id, support_id)

        self._event_repository.update(event)

        return event
