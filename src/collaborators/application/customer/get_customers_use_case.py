from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.customer.customer_repository_abc import CustomerRepositoryABC


class GetCustomersUseCase(UseCaseABC):
    permissions = Permissions.READ_CUSTOMERS

    def __init__(self, auth_context: AuthContextABC, repository: CustomerRepositoryABC):
        super().__init__(auth_context)
        self.repository = repository

    def _execute(self):
        customers = self.repository.get_all()
        return customers
