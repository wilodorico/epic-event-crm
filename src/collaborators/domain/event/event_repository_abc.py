from abc import ABC, abstractmethod

from collaborators.domain.event.event import Event


class EventRepositoryABC(ABC):
    @abstractmethod
    def create(self, event: Event) -> Event | None: ...
