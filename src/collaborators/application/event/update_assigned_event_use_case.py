from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.event.event_repository_abc import EventRepositoryABC


class UpdateAssignedEventUseCase(UseCaseABC):
    permissions = Permissions.UPDATE_EVENT

    def __init__(self, auth_context: AuthContextABC, event_repository: EventRepositoryABC):
        super().__init__(auth_context)
        self._event_repository = event_repository

    def _execute(self, event_id, **updates):
        event = self._event_repository.find_by_id(event_id)

        if not event:
            raise ValueError("Event not found")

        event.update(updates)
        self._event_repository.update(event)

        return event
