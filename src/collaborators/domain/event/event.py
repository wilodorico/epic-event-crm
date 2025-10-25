from datetime import datetime
from typing import TypedDict

from commons.clock_abc import ClockABC


class EventUpdateData(TypedDict, total=False):
    title: str
    date_start: datetime
    date_end: datetime
    location: str
    attendees: int
    notes: str


class Event:
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
        clock: ClockABC | None = None,
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
        self.created_at = clock.now() if clock else datetime.now()
        self.updated_at = clock.now() if clock else datetime.now()
        self.updated_by_id = None
        self._clock = clock

    def assign_support(self, collaborator_id: str, support_id: str):
        self.contact_support_id = support_id
        self.updated_at = self._clock.now() if self._clock else datetime.now()
        self.updated_by_id = collaborator_id

    def update(self, data: EventUpdateData, updater_id: str):
        """Update allowed fields only"""
        for field, value in data.items():
            setattr(self, field, value)
        self.updated_at = self._clock.now() if self._clock else datetime.now()
        self.updated_by_id = updater_id

    def is_assigned_to_support(self) -> bool:
        return self.contact_support_id is not None

    def is_past_event(self) -> bool:
        return self.date_end < datetime.now()
