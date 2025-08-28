from datetime import datetime


class Customer:
    def __init__(
        self,
        id: str,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        company: str,
        commercial_contact: str,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.company = company
        self.commercial_contact = commercial_contact
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
