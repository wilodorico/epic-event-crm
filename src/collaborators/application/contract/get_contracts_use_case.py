from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC


class GetContractsUseCase:
    def __init__(self, repository: ContractRepositoryABC, auth_context: AuthContextABC):
        self.repository = repository
        self.auth_context = auth_context

    def execute(self):
        self.auth_context.ensure(Permissions.READ_CONTRACTS)

        contracts = self.repository.get_all()
        return contracts
