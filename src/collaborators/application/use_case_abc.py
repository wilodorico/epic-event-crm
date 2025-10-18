from abc import ABC, abstractmethod
from typing import Optional

from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.permissions import Permissions


class UseCaseABC(ABC):
    """
    Abstract base class for all application use cases.

    This class defines a consistent execution flow:
      - Validates user permissions through the AuthContext.
      - Delegates the actual business logic to the `_execute` method,
        which must be implemented by subclasses.

    Subclasses should:
      - Define the required `permissions` class attribute.
      - Implement the `_execute` method containing the business logic.

    Example:
        class GetEventsUseCase(UseCaseABC):
            permissions = Permissions.READ_EVENTS

            def __init__(self, event_repository, auth_context):
                super().__init__(auth_context)
                self._event_repository = event_repository

            def _execute(self):
                return self._event_repository.get_all()
    """

    permissions: Optional[Permissions] = None

    def __init__(self, auth_context: AuthContextABC):
        self._auth_context = auth_context

    @abstractmethod
    def _execute(self, *args, **kwargs):
        pass

    def execute(self, *args, **kwargs):
        # TODO: Implement Log with Sentry
        # self.__class__.__name__
        self._auth_context.ensure(self.permissions)
        return self._execute(*args, **kwargs)
