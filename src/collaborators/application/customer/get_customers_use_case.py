from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.customer.customer_repository_abc import CustomerRepositoryABC


class GetCustomersUseCase:
    def __init__(self, repository: CustomerRepositoryABC, auth_context: AuthContextABC):
        self.repository = repository
        self.auth_context = auth_context

    def execute(self):
        self.auth_context.ensure(Permissions.READ_CUSTOMERS)

        customers = self.repository.get_all()
        return customers
