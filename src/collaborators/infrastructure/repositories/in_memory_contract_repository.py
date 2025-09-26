from collaborators.domain.contract.contract import Contract
from collaborators.domain.contract.contract_repository_abc import ContractRepositoryABC


class InMemoryContractRepository(ContractRepositoryABC):
    def __init__(self):
        self.contracts = {}

    def create(self, contract: Contract) -> None:
        self.contracts[contract.id] = contract

    def find_by_id(self, contract_id: str) -> Contract | None:
        return self.contracts.get(contract_id)

    def find_by_customer_id(self, customer_id: str) -> list[Contract] | None:
        return [contract for contract in self.contracts.values() if contract.customer_id == customer_id] or None

    def update(self, contract: Contract) -> None:
        self.contracts[contract.id] = contract

    def count(self) -> int:
        return len(self.contracts)

    def get_all(self) -> list[Contract] | list:
        return list(self.contracts.values())
