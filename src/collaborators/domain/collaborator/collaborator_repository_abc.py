from abc import ABC, abstractmethod

from collaborators.domain.collaborator.collaborator import Collaborator


class CollaboratorRepositoryABC(ABC):
    @abstractmethod
    def create(self, collaborator: Collaborator) -> None: ...

    @abstractmethod
    def find_by_email(self, email: str) -> Collaborator | None: ...
