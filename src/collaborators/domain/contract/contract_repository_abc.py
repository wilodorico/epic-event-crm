from abc import ABC, abstractmethod

from collaborators.domain.contract.contract import Contract


class ContractRepositoryABC(ABC):
    @abstractmethod
    def create(self, contract: Contract) -> None: ...

    @abstractmethod
    def find_by_id(self, contract_id: str) -> Contract | None: ...
