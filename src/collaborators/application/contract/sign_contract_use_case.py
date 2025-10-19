from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC


class SignContractUseCase(UseCaseABC):
    permissions = Permissions.SIGN_CONTRACT

    def __init__(self, auth_context: AuthContextABC, repository: ContractRepositoryABC):
        super().__init__(auth_context)
        self.repository = repository

    def _execute(self, updater_id: str, contract_id: str) -> None:
        contract = self.repository.find_by_id(contract_id)
        if not contract:
            raise ValueError("Contract not found.")

        if contract.is_signed():
            raise ValueError("Contract is already signed.")

        contract.sign_contract(updater_id)

        self.repository.update(contract)
