from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract import Contract
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC


class GetUnsignedContractsUseCase(UseCaseABC):
    permissions = Permissions.FILTER_CONTRACTS

    def __init__(self, auth_context: AuthContextABC, repository: ContractRepositoryABC):
        super().__init__(auth_context)
        self._repository = repository

    def _execute(self, commercial_id: str) -> list[Contract]:
        unsigned_contracts = self._repository.get_all_unsigned(commercial_id)
        return unsigned_contracts
