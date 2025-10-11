from datetime import datetime


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
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.updated_by_id = None
