from collaborators.application.services.auth_context import AuthContext
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract import Contract
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC


class UpdateContractUseCase(UseCaseABC):
    permissions = Permissions.UPDATE_CONTRACT

    def __init__(
        self,
        auth_context: AuthContext,
        contract_repository: ContractRepositoryABC,
    ):
        super().__init__(auth_context)
        self._contract_repository = contract_repository

    def _execute(self, updater: Collaborator, contract_id: str, data: dict) -> Contract | None:
        contract = self._contract_repository.find_by_id(contract_id)

        if not contract:
            raise ValueError("Contract not found.")

        if updater.role == Role.COMMERCIAL and contract.commercial_id != updater.id:
            raise PermissionError("Commercial can only update their own customers contracts")

        contract.update(data, updater.id)

        self._contract_repository.update(contract)

        return contract
