from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.event.event_repository_abc import EventRepositoryABC


class UpdateAssignedEventUseCase(UseCaseABC):
    """Handles the update of an event by the assigned support contact.

    This use case ensures that only the support contact assigned to an event can update it.
    It validates the event's existence, assignment status, ownership, and ensures that only
    future events can be modified. The changes are then saved to the repository.

    Requires the UPDATE_EVENT permission to execute.
    """

    permissions = Permissions.UPDATE_EVENT

    def __init__(self, auth_context: AuthContextABC, event_repository: EventRepositoryABC):
        super().__init__(auth_context)
        self._event_repository = event_repository

    def _execute(self, event_id, **data):
        """Updates and persists an assigned event entity.

        Args:
            event_id: The unique identifier of the event to update.
            **data: Keyword arguments containing the fields to update and their new values.

        Raises:
            ValueError: If the event is not found.
            PermissionError: If the user lacks permissions, if the event is not assigned
                to any support contact, if the event is assigned to another support contact,
                or if attempting to update a past event.

        Returns:
            Event: The updated event entity.
        """
        support_id = self._auth_context.user.id
        event = self._event_repository.find_by_id(event_id)

        if not event:
            raise ValueError("Event not found")

        if not event.is_assigned_to_support():
            raise PermissionError("Event not assigned to any support collaborator")

        if event.contact_support_id != support_id:
            raise PermissionError("Event assigned to another support collaborator")

        if event.is_past_event():
            raise PermissionError("Cannot update past events")

        event.update(data, updater_id=support_id)
        self._event_repository.update(event)

        return event
