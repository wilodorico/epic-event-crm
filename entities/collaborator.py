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
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        phone_number: str,
        role: Role,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.role = role
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
