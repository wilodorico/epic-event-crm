from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.event.event_repository_abc import EventRepositoryABC


class GetEventsUseCase:
    def __init__(self, event_repository: EventRepositoryABC, auth_context: AuthContextABC):
        self._event_repository = event_repository
        self._auth_context = auth_context

    def execute(self):
        self._auth_context.ensure(Permissions.READ_EVENTS)
        return self._event_repository.get_all()
