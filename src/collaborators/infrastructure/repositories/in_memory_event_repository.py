from collaborators.domain.event.event import Event
from collaborators.domain.event.event_repository_abc import EventRepositoryABC


class InMemoryEventRepository(EventRepositoryABC):
    def __init__(self):
        self.events: dict[str, Event] = {}

    def create(self, event: Event) -> Event | None:
        self.events[event.id] = event
        return event

    def get_all(self) -> list[Event]:
        return list(self.events.values())

    def count(self) -> int:
        return len(self.events)
