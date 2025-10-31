from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.customer.customer import Customer
from collaborators.domain.customer.customer_repository_abc import CustomerRepositoryABC
from commons.id_generator_abc import IdGeneratorABC


class CreateCustomerUseCase(UseCaseABC):
    """Handles the creation of a new customer by an authorized collaborator.

    This use case ensures that the customer email is unique, automatically assigns
    the creator as the commercial contact, and saves the new customer record to
    the repository.

    Requires the CREATE_CUSTOMER permission to execute.
    """

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
        """Creates and persists a new customer entity.

        Args:
            creator: The collaborator performing the operation.
            first_name: The customer's first name.
            last_name: The customer's last name.
            email: The customer's unique email address.
            phone_number: The customer's phone number.
            company: The name of the company the customer belongs to.

        Raises:
            ValueError: If the email address already exists.
            PermissionError: If the user lacks permissions.

        Returns:
            Customer: The newly created customer with the creator as commercial contact.
        """
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
