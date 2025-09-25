from abc import ABC, abstractmethod

from collaborators.domain.contract.contract import Contract


class ContractRepositoryABC(ABC):
    @abstractmethod
    def create(self, contract: Contract) -> None: ...

    @abstractmethod
    def find_by_id(self, contract_id: str) -> Contract | None: ...

    @abstractmethod
    def find_by_customer_id(self, customer_id: str) -> list[Contract] | None: ...

    @abstractmethod
    def update(self, contract: Contract) -> None: ...
