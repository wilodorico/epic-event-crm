from collaborators.domain.event.event import Event
from collaborators.infrastructure.database.models.event import EventModel


class EventMapper:
    @staticmethod
    def to_entity(model: EventModel) -> Event:
        event = Event(
            id=model.id,
            title=model.title,
            customer_id=model.customer_id,
            contract_id=model.contract_id,
            date_start=model.date_start,
            date_end=model.date_end,
            location=model.location,
            attendees=model.attendees,
            notes=model.notes,
        )
        # Override the auto-generated timestamps with DB values
        event.created_at = model.created_at
        event.updated_at = model.updated_at
        event.updated_by_id = model.updated_by_id
        return event

    @staticmethod
    def to_model(entity: Event) -> EventModel:
        model = EventModel(
            id=entity.id,
            title=entity.title,
            customer_id=entity.customer_id,
            contract_id=entity.contract_id,
            date_start=entity.date_start,
            date_end=entity.date_end,
            location=entity.location,
            attendees=entity.attendees,
            notes=entity.notes,
            updated_by_id=entity.updated_by_id,
        )
        # Set timestamps manually if they exist
        if entity.created_at:
            model.created_at = entity.created_at
        if entity.updated_at:
            model.updated_at = entity.updated_at
        return model
