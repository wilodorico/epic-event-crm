from datetime import datetime
from enum import Enum
from typing import TypedDict


class Role(Enum):
    COMMERCIAL = "Commercial"
    MANAGEMENT = "Management"
    SUPPORT = "Support"


class CollaboratorUpdateData(TypedDict, total=False):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    role: Role


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

    def update(self, data: CollaboratorUpdateData, updater_id: str):
        for field, value in data.items():
            if field == "role" and isinstance(value, str):
                value = Role(value)
            setattr(self, field, value)
        self.updated_at = datetime.now()
        self.updated_by_id = updater_id
