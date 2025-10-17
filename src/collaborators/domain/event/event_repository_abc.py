from abc import ABC, abstractmethod

from collaborators.domain.event.event import Event


class EventRepositoryABC(ABC):
    @abstractmethod
    def create(self, event: Event) -> Event | None: ...

    @abstractmethod
    def get_all(self) -> list[Event]: ...

    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def get_all_unassigned(self) -> list[Event]: ...

    @abstractmethod
    def find_by_id(self, event_id: str) -> Event | None: ...

    @abstractmethod
    def update(self, event: Event) -> None: ...
