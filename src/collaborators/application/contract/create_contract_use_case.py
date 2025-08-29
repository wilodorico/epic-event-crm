from decimal import Decimal

from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract import Contract
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC
from collaborators.domain.customer.customer_repository_abc import CustomerRepositoryABC
from commons.id_generator_abc import IdGeneratorABC


class CreateContractUseCase:
    def __init__(
        self,
        customer_repository: CustomerRepositoryABC,
        contract_repository: ContractRepositoryABC,
        id_generator: IdGeneratorABC,
        auth_context: AuthContextABC,
    ):
        self._customer_repository = customer_repository
        self._contract_repository = contract_repository
        self._id_generator = id_generator
        self._auth_context = auth_context

    def execute(
        self,
        creator: Collaborator,
        customer_id: str,
        commercial_id: str,
        total_amount: Decimal,
        remaining_amount: Decimal,
    ) -> Contract:
        self._auth_context.ensure(Permissions.CREATE_CONTRACT)

        customer = self._customer_repository.find_by_id(customer_id)

        if customer is None:
            raise ValueError("Customer does not exist")

        id = self._id_generator.generate()

        contract = Contract(
            id=id,
            customer_id=customer_id,
            commercial_id=commercial_id,
            created_by_id=creator.id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
        )

        self._contract_repository.create(contract)

        return contract
