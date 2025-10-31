from datetime import datetime
from typing import TypedDict


class EventUpdateData(TypedDict, total=False):
    """Typed dictionary for updating event data.

    Used to pass partial updates to an `Event` instance.
    All fields are optional.
    """

    title: str
    date_start: datetime
    date_end: datetime
    location: str
    attendees: int
    notes: str


class Event:
    """Domain entity representing an event organized for a customer.

    An event is created from a signed contract and managed by a commercial contact.
    It can be assigned to a support contact who will handle the event logistics and
    execution. Events track scheduling, location, attendees, and organizational notes.
    """

    def __init__(
        self,
        id: str,
        title: str,
        customer_id: str,
        contract_id: str,
        date_start: datetime,
        date_end: datetime,
        location: str,
        attendees: int,
        notes: str,
    ):
        self.id = id
        self.title = title
        self.customer_id = customer_id
        self.contract_id = contract_id
        self.date_start = date_start
        self.date_end = date_end
        self.location = location
        self.attendees = attendees
        self.notes = notes
        self.contact_support_id = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.updated_by_id = None

    def assign_support(self, collaborator_id: str, support_id: str):
        """Assigns a support contact to the event.

        Args:
            collaborator_id: ID of the user performing the assignment (usually a manager).
            support_id: ID of the support contact to assign to the event.

        Note:
            Updates `contact_support_id`, `updated_at`, and `updated_by_id` on success.
        """
        self.contact_support_id = support_id
        self.updated_at = datetime.now()
        self.updated_by_id = collaborator_id

    def update(self, data: EventUpdateData, updater_id: str):
        """Updates the event's data with the provided fields.

        Args:
            data: Fields to update (as `EventUpdateData`).
            updater_id: ID of the user performing the update.

        Note:
            Updates `updated_at` and `updated_by_id` on success.
        """
        for field, value in data.items():
            setattr(self, field, value)
        self.updated_at = datetime.now()
        self.updated_by_id = updater_id

    def is_assigned_to_support(self) -> bool:
        """Checks if the event has a support contact assigned.

        Returns:
            bool: True if a support contact is assigned, False otherwise.
        """
        return self.contact_support_id is not None

    def is_past_event(self) -> bool:
        """Checks if the event has already ended.

        Returns:
            bool: True if the event end date is in the past, False otherwise.
        """
        return self.date_end < datetime.now()
