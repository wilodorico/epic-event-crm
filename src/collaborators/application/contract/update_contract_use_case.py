from collaborators.application.services.auth_context import AuthContext
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract import Contract
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC


class UpdateContractUseCase(UseCaseABC):
    """Handles the update of a contract by an authorized collaborator.

    This use case ensures that only authorized collaborators can update contracts. For commercial
    contacts, it restricts updates to their own customers' contracts only. It validates
    the contract's existence, applies the provided changes, and persists the updated
    contract in the repository.

    Requires the UPDATE_CONTRACT permission to execute.
    """

    permissions = Permissions.UPDATE_CONTRACT

    def __init__(
        self,
        auth_context: AuthContext,
        contract_repository: ContractRepositoryABC,
    ):
        super().__init__(auth_context)
        self._contract_repository = contract_repository

    def _execute(self, updater: Collaborator, contract_id: str, data: dict) -> Contract | None:
        """Updates a contract's information.

        Args:
            updater: The collaborator performing the update (manager or commercial contact).
            contract_id: The unique identifier of the contract to update.
            data: Dictionary containing the fields to update and their new values.

        Raises:
            ValueError: If the contract is not found.
            PermissionError: If the user lacks permissions or if a commercial contact
                attempts to update a contract not assigned to them.

        Returns:
            Contract | None: The updated contract entity persisted in the repository.
        """
        contract = self._contract_repository.find_by_id(contract_id)

        if not contract:
            raise ValueError("Contract not found.")

        if updater.role == Role.COMMERCIAL and contract.commercial_id != updater.id:
            raise PermissionError("Commercial can only update their own customers contracts")

        contract.update(data, updater.id)

        self._contract_repository.update(contract)

        return contract
