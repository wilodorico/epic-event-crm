from datetime import datetime
from typing import TypedDict


class CustomerUpdateData(TypedDict, total=False):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    company: str


class Customer:
    def __init__(
        self,
        id: str,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        company: str,
        commercial_contact_id: str,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.company = company
        self.commercial_contact_id = commercial_contact_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, data: CustomerUpdateData):
        """Update allowed fields only"""
        for field, value in data.items():
            setattr(self, field, value)
        self.updated_at = datetime.now()
