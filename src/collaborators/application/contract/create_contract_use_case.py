from decimal import Decimal

from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract import Contract
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC
from collaborators.domain.customer.customer_repository_abc import CustomerRepositoryABC
from commons.id_generator_abc import IdGeneratorABC


class CreateContractUseCase(UseCaseABC):
    """Handles the creation of a new contract by a manager.

    This use case ensures that only authorized managers can create contracts for existing customers.
    It validates the customer's existence, associates the contract with the customer's commercial contact,
    and persists the new contract record in the repository.

    Requires the CREATE_CONTRACT permission to execute.
    """

    permissions = Permissions.CREATE_CONTRACT

    def __init__(
        self,
        auth_context: AuthContextABC,
        customer_repository: CustomerRepositoryABC,
        contract_repository: ContractRepositoryABC,
        id_generator: IdGeneratorABC,
    ):
        super().__init__(auth_context)
        self._customer_repository = customer_repository
        self._contract_repository = contract_repository
        self._id_generator = id_generator

    def _execute(
        self,
        creator: Collaborator,
        customer_id: str,
        total_amount: Decimal,
        remaining_amount: Decimal,
    ) -> Contract:
        """Creates a new contract for a customer.

        Args:
            creator: The collaborator performing the creation (usually a manager).
            customer_id: The unique identifier of the customer for whom the contract is created.
            total_amount: The total contract value.
            remaining_amount: The outstanding amount to be paid.

        Raises:
            ValueError: If the customer does not exist.
            PermissionError: If the creator lacks permissions.

        Returns:
            Contract: The newly created contract entity.
        """
        customer = self._customer_repository.find_by_id(customer_id)

        if customer is None:
            raise ValueError("Customer does not exist")

        id = self._id_generator.generate()

        contract = Contract(
            id=id,
            customer_id=customer_id,
            commercial_id=customer.commercial_contact_id,
            created_by_id=creator.id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
        )

        self._contract_repository.create(contract)

        return contract
