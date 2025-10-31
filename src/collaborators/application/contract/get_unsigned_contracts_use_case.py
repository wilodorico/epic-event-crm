from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract import Contract
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC


class GetUnsignedContractsUseCase(UseCaseABC):
    """Handles the retrieval of unsigned contracts for a specific commercial contact.

    This use case ensures that only authorized users can filter and view contracts that
    have not been signed yet. It retrieves contracts associated with a commercial contact
    that are still awaiting signature.

    Requires the FILTER_CONTRACTS permission to execute.
    """

    permissions = Permissions.FILTER_CONTRACTS

    def __init__(self, auth_context: AuthContextABC, repository: ContractRepositoryABC):
        super().__init__(auth_context)
        self._repository = repository

    def _execute(self, commercial_id: str) -> list[Contract]:
        """Retrieves all unsigned contracts for a commercial contact.

        Args:
            commercial_id: The unique identifier of the commercial contact.

        Raises:
            PermissionError: If the user lacks permissions.

        Returns:
            list[Contract]: A list of contract entities awaiting signature.
        """
        unsigned_contracts = self._repository.get_all_unsigned(commercial_id)
        return unsigned_contracts
