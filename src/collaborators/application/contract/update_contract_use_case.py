from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract import Contract
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC


class UpdateContractUseCase:
    def __init__(
        self,
        contract_repository: ContractRepositoryABC,
        auth_context: AuthContext,
    ):
        self._contract_repository = contract_repository
        self._auth_context = auth_context

    def execute(self, updater: Collaborator, contract_id: str, data: dict) -> Contract | None:
        self._auth_context.ensure(Permissions.UPDATE_CONTRACT)

        contract = self._contract_repository.find_by_id(contract_id)

        if not contract:
            raise ValueError("Contract not found.")

        contract.update(data, updater.id)

        self._contract_repository.update(contract)

        return contract
