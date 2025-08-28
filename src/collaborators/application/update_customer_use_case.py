from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.customer.customer_repository_abc import CustomerRepositoryABC
from commons.id_generator_abc import IdGeneratorABC


class UpdateCustomerUseCase:
    def __init__(self, repository: CustomerRepositoryABC, id_generator: IdGeneratorABC, auth_context: AuthContextABC):
        self._repository = repository
        self._id_generator = id_generator
        self._auth_context = auth_context

    def execute(self, updater: Collaborator, customer_id: str, data: dict) -> Collaborator:
        self._auth_context.ensure(Permissions.UPDATE_CUSTOMER)

        customer = self._repository.find_by_id(customer_id)

        customer.update(data, updater.id)
        self._repository.update(customer)

        return customer
