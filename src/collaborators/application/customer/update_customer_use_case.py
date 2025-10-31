from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.customer.customer_repository_abc import CustomerRepositoryABC


class UpdateCustomerUseCase(UseCaseABC):
    """Handles the update of customer information by an authorized collaborator.

    This use case ensures that commercial contacts can only update their own customers.
    It validates the customer's existence and ownership, applies the changes, and saves
    the updated customer record to the repository.

    Requires the UPDATE_CUSTOMER permission to execute.
    """

    permissions = Permissions.UPDATE_CUSTOMER

    def __init__(self, auth_context: AuthContextABC, repository: CustomerRepositoryABC):
        super().__init__(auth_context)
        self._repository = repository

    def _execute(self, updater: Collaborator, customer_id: str, data: dict) -> Collaborator:
        """Updates and persists a customer entity.

        Args:
            updater: The collaborator performing the operation.
            customer_id: The unique identifier of the customer to update.
            data: A dictionary containing the fields to update and their new values.

        Raises:
            ValueError: If the customer is not found.
            PermissionError: If the user lacks permissions or attempts to update
                a customer not assigned to them.

        Returns:
            Collaborator: The updated customer entity.
        """
        customer = self._repository.find_by_id(customer_id)

        if not customer:
            raise ValueError("Customer not found.")

        if customer.commercial_contact_id != updater.id:
            raise PermissionError("You can only update your own customers")

        customer.update(data)
        self._repository.update(customer)

        return customer
