from abc import ABC, abstractmethod

from collaborators.domain.collaborator.collaborator import Collaborator


class CollaboratorRepositoryABC(ABC):
    @abstractmethod
    def create(self, collaborator: Collaborator) -> None: ...

    @abstractmethod
    def find_by_email(self, email: str) -> Collaborator | None: ...

    @abstractmethod
    def find_by_id(self, collaborator_id: str) -> Collaborator | None: ...

    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def update(self, collaborator: Collaborator) -> None: ...

    @abstractmethod
    def delete(self, collaborator_id: str) -> None: ...
