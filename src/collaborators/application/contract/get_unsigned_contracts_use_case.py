from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract import Contract
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC


class GetUnsignedContractsUseCase:
    def __init__(self, repository: ContractRepositoryABC, auth_context: AuthContextABC):
        self._repository = repository
        self._auth_context = auth_context

    def execute(self, commercial_id: str) -> list[Contract]:
        self._auth_context.ensure(Permissions.FILTER_CONTRACTS)

        unsigned_contracts = self._repository.get_all_unsigned(commercial_id)
        return unsigned_contracts
