from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC


class GetContractsUseCase(UseCaseABC):
    """Handles the retrieval of all contracts.

    This use case ensures that only authorized users can view all contracts in the system.
    It fetches and returns the complete list of contracts from the repository.

    Requires the READ_CONTRACTS permission to execute.
    """

    permissions = Permissions.READ_CONTRACTS

    def __init__(self, auth_context: AuthContextABC, repository: ContractRepositoryABC):
        super().__init__(auth_context)
        self.repository = repository

    def _execute(self):
        """Retrieves all contracts.

        Args:
            None

        Raises:
            PermissionError: If the user lacks permissions.

        Returns:
            list[Contract]: A list of all contract entities in the system.
        """
        contracts = self.repository.get_all()
        return contracts
