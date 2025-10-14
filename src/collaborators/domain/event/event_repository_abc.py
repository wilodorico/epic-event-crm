from abc import ABC, abstractmethod

from collaborators.domain.event.event import Event


class EventRepositoryABC(ABC):
    @abstractmethod
    def create(self, event: Event) -> Event | None: ...

    @abstractmethod
    def get_all(self) -> list[Event]: ...

    @abstractmethod
    def count(self) -> int: ...
