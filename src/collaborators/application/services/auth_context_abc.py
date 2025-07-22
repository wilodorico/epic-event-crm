from abc import ABC, abstractmethod

from collaborators.domain.collaborator.permissions import Permissions


class AuthContextABC(ABC):
    @abstractmethod
    def can(self, permission: Permissions) -> bool: ...

    @abstractmethod
    def ensure(self, permission: Permissions) -> None: ...
