from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.customer.customer_repository_abc import CustomerRepositoryABC


class UpdateCustomerUseCase:
    def __init__(self, repository: CustomerRepositoryABC, auth_context: AuthContextABC):
        self._repository = repository
        self._auth_context = auth_context

    def execute(self, updater: Collaborator, customer_id: str, data: dict) -> Collaborator:
        self._auth_context.ensure(Permissions.UPDATE_CUSTOMER)

        customer = self._repository.find_by_id(customer_id)

        if not customer:
            raise ValueError("Customer not found.")

        if customer.commercial_contact_id != updater.id:
            raise PermissionError("You can only update your own customers")

        customer.update(data)
        self._repository.update(customer)

        return customer
