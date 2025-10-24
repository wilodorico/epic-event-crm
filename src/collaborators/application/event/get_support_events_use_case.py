from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.event.event_repository_abc import EventRepositoryABC


class GetSupportEventsUseCase(UseCaseABC):
    permissions = Permissions.READ_EVENTS

    def __init__(self, auth_context: AuthContextABC, event_repository: EventRepositoryABC):
        super().__init__(auth_context)
        self._event_repository = event_repository

    def _execute(self, support_id):
        return self._event_repository.get_by_support_id(support_id)
