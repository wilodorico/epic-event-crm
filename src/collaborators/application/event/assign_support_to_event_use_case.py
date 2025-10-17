from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.event.event_repository_abc import EventRepositoryABC


class GetAssignSupportToEventUseCase:
    def __init__(self, event_repository: EventRepositoryABC, auth_context: AuthContextABC):
        self._event_repository = event_repository
        self._auth_context = auth_context

    def execute(self, collaborator: Collaborator, event_id: str, support_id: str):
        self._auth_context.ensure(Permissions.ASSIGN_EVENT)

        event = self._event_repository.find_by_id(event_id)

        if not event:
            raise ValueError("Event not found.")

        event.assign_support(collaborator.id, support_id)

        self._event_repository.update(event)

        return event
