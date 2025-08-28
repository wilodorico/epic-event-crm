from abc import ABC, abstractmethod

from collaborators.domain.customer.customer import Customer


class CustomerRepositoryABC(ABC):
    @abstractmethod
    def create(self, customer: Customer) -> None: ...

    @abstractmethod
    def update(self, customer: Customer) -> None: ...

    @abstractmethod
    def find_by_email(self, email: str) -> Customer | None: ...

    @abstractmethod
    def find_by_id(self, customer_id: str) -> Customer | None: ...
