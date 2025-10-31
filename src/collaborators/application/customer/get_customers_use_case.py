from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.customer.customer_repository_abc import CustomerRepositoryABC


class GetCustomersUseCase(UseCaseABC):
    """Handles the retrieval of all customers in the system.

    This use case ensures that only authorized users can view the complete list
    of customers and returns all customer records from the repository.

    Requires the READ_CUSTOMERS permission to execute.
    """

    permissions = Permissions.READ_CUSTOMERS

    def __init__(self, auth_context: AuthContextABC, repository: CustomerRepositoryABC):
        super().__init__(auth_context)
        self.repository = repository

    def _execute(self):
        """Retrieves and returns all customer entities.

        Args:
            None

        Raises:
            PermissionError: If the user lacks permissions.

        Returns:
            list[Customer]: A list of all customer entities in the system.
        """
        customers = self.repository.get_all()
        return customers
