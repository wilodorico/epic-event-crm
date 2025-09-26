from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract import ContractStatus
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC


class SignContractUseCase:
    def __init__(self, repository: ContractRepositoryABC, auth_context: AuthContextABC):
        self.repository = repository
        self.auth_context = auth_context

    def execute(self, updater_id: str, contract_id: str) -> None:
        self.auth_context.ensure(Permissions.SIGN_CONTRACT)
        contract = self.repository.find_by_id(contract_id)
        if not contract:
            raise ValueError("Contract not found.")

        if contract.status == ContractStatus.SIGNED:
            raise ValueError("Contract is already signed.")

        contract.sign_contract(updater_id)

        self.repository.update(contract)
