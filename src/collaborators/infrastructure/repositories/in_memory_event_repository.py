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

    def get_all_unassigned(self) -> list[Event]:
        return [event for event in self.events.values() if not event.contact_support_id]

    def find_by_id(self, event_id: str) -> Event | None:
        return self.events.get(event_id)

    def update(self, event: Event) -> None:
        self.events[event.id] = event
