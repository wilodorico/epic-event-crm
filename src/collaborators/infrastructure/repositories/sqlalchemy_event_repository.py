from sqlalchemy.orm import Session

from collaborators.domain.event.event import Event
from collaborators.infrastructure.mappers.event import EventMapper


class SqlalchemyEventRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, event: Event) -> Event | None:
        model = EventMapper.to_model(event)
        self.session.add(model)
        self.session.commit()
        return event
