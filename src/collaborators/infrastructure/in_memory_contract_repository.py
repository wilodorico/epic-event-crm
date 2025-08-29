from collaborators.domain.contract.contract import Contract
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC


class InMemoryContractRepository(ContractRepositoryABC):
    def __init__(self):
        self.contracts = {}

    def create(self, contract: Contract) -> Contract | None:
        self.contracts[contract.id] = contract
        return contract

    def find_by_id(self, contract_id: str) -> Contract | None:
        return self.contracts.get(contract_id)
