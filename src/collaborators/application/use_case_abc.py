from abc import ABC, abstractmethod
from typing import Optional

from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.sentry_config import capture_exception


class UseCaseABC(ABC):
    """
    Abstract base class for all application use cases.

    This class defines a consistent execution flow:
      - Validates user permissions through the AuthContext.
      - Delegates the actual business logic to the `_execute` method,
        which must be implemented by subclasses.
      - Captures and logs any unexpected exceptions to Sentry.

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
        """Executes the use case with permission validation and error tracking.

        This method orchestrates the use case execution by:
        1. Validating user permissions
        2. Executing the business logic
        3. Capturing any unexpected exceptions to Sentry

        Args:
            *args: Positional arguments passed to the _execute method.
            **kwargs: Keyword arguments passed to the _execute method.

        Returns:
            The result of the _execute method.

        Raises:
            AuthorizationError: If the user lacks required permissions.
            Exception: Any exception raised by the _execute method (after logging to Sentry).
        """
        try:
            self._auth_context.ensure(self.permissions)
            return self._execute(*args, **kwargs)
        except Exception as e:
            # Capture unexpected exceptions to Sentry with use case context
            capture_exception(
                e,
                use_case=self.__class__.__name__,
                permission=self.permissions.value if self.permissions else None,
                user_id=getattr(self._auth_context.user, "id", None) if hasattr(self._auth_context, "user") else None,
            )
            # Re-raise the exception to maintain normal error handling flow
            raise
