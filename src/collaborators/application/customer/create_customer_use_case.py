from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.customer.customer import Customer
from collaborators.domain.customer.customer_repository_abc import CustomerRepositoryABC
from commons.id_generator_abc import IdGeneratorABC


class CreateCustomerUseCase(UseCaseABC):
    permissions = Permissions.CREATE_CUSTOMER

    def __init__(self, auth_context: AuthContextABC, repository: CustomerRepositoryABC, id_generator: IdGeneratorABC):
        super().__init__(auth_context)
        self._repository = repository
        self._id_generator = id_generator

    def _execute(
        self,
        creator: Collaborator,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        company: str,
    ) -> Customer:
        if self._repository.find_by_email(email):
            raise ValueError("Email already exists")

        id = self._id_generator.generate()

        customer = Customer(
            id=id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            company=company,
            commercial_contact_id=creator.id,
        )
        self._repository.create(customer)

        return customer
