from sqlalchemy import select
from sqlalchemy.orm import Session

from collaborators.domain.event.event import Event
from collaborators.domain.event.event_repository_abc import EventRepositoryABC
from collaborators.infrastructure.database.models.event import EventModel
from collaborators.infrastructure.mappers.event import EventMapper


class SqlalchemyEventRepository(EventRepositoryABC):
    def __init__(self, session: Session):
        self.session = session

    def create(self, event: Event) -> Event | None:
        model = EventMapper.to_model(event)
        self.session.add(model)
        self.session.commit()
        return event

    def get_all(self) -> list[Event]:
        query = select(EventModel)
        result = self.session.execute(query)
        event_models = result.scalars().all()
        return [EventMapper.to_entity(model) for model in event_models]

    def count(self) -> int:
        query = select(EventModel)
        result = self.session.execute(query)
        return len(result.scalars().all())

    def get_all_unassigned(self) -> list[Event]:
        query = select(EventModel).where(EventModel.contact_support_id.is_(None))
        result = self.session.execute(query)
        unassigned_event_models = result.scalars().all()
        return [EventMapper.to_entity(model) for model in unassigned_event_models]

    def find_by_id(self, event_id: str) -> Event | None:
        query = select(EventModel).where(EventModel.id == event_id)
        result = self.session.execute(query)
        event_model = result.scalars().first()
        if event_model:
            return EventMapper.to_entity(event_model)
        return None

    def update(self, event: Event) -> None:
        """Update an existing event."""
        model = EventMapper.to_model(event)
        # Merge updates the existing record with the same primary key
        self.session.merge(model)
        self.session.commit()
