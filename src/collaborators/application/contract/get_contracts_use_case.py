from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC


class GetContractsUseCase(UseCaseABC):
    permissions = Permissions.READ_CONTRACTS

    def __init__(self, auth_context: AuthContextABC, repository: ContractRepositoryABC):
        super().__init__(auth_context)
        self.repository = repository

    def _execute(self):
        contracts = self.repository.get_all()
        return contracts
