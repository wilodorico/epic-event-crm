from datetime import datetime
from enum import Enum


class Role(Enum):
    MARKETING = "Marketing"
    MANAGEMENT = "Management"
    SUPPORT = "Support"


class Collaborator:
    def __init__(
        self,
        id: str,
        created_by_id: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        phone_number: str,
        role: Role,
    ):
        self.id = id
        self.created_by_id = created_by_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.role = role
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.updated_by_id = None

    def update(self, data: dict, updater_id: str):
        for field in ["first_name", "last_name", "email", "phone_number", "role"]:
            if field in data:
                value = data[field]
                if field == "role" and isinstance(value, str):
                    value = Role(value)
                setattr(self, field, value)
        self.updated_at = datetime.now()
        self.updated_by_id = updater_id
