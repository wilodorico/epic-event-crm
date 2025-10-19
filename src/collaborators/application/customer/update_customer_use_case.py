from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.customer.customer_repository_abc import CustomerRepositoryABC


class UpdateCustomerUseCase(UseCaseABC):
    permissions = Permissions.UPDATE_CUSTOMER

    def __init__(self, auth_context: AuthContextABC, repository: CustomerRepositoryABC):
        super().__init__(auth_context)
        self._repository = repository

    def _execute(self, updater: Collaborator, customer_id: str, data: dict) -> Collaborator:
        customer = self._repository.find_by_id(customer_id)

        if not customer:
            raise ValueError("Customer not found.")

        if customer.commercial_contact_id != updater.id:
            raise PermissionError("You can only update your own customers")

        customer.update(data)
        self._repository.update(customer)

        return customer
