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
            date_start=model.start_date,
            date_end=model.end_date,
            location=model.location,
            attendees=model.attendee,
            notes=model.notes,
        )
        event.contact_support_id = model.contact_support_id

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
            start_date=entity.date_start,
            end_date=entity.date_end,
            location=entity.location,
            attendee=entity.attendees,
            notes=entity.notes,
            contact_support_id=entity.contact_support_id,
            updated_by_id=entity.updated_by_id,
        )
        # Set timestamps manually if they exist
        if entity.created_at:
            model.created_at = entity.created_at
        if entity.updated_at:
            model.updated_at = entity.updated_at
        return model
