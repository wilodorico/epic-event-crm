from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.customer.customer import Customer
from collaborators.domain.customer.customer_repository_abc import CustomerRepositoryABC
from commons.id_generator_abc import IdGeneratorABC


class CreateCustomerUseCase:
    def __init__(self, repository: CustomerRepositoryABC, id_generator: IdGeneratorABC, auth_context: AuthContextABC):
        self._repository = repository
        self._id_generator = id_generator
        self._auth_context = auth_context

    def execute(
        self,
        creator: Collaborator,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        entreprise: str,
    ) -> None:
        self._auth_context.ensure(Permissions.CREATE_CUSTOMER)

        if self._repository.find_by_email(email):
            raise ValueError("Email already exists")

        id = self._id_generator.generate()

        customer = Customer(
            id=id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            entreprise=entreprise,
            commercial_contact=creator.id,
        )
        self._repository.create(customer)

        return customer
