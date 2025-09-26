from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TypedDict


class ContractStatus(Enum):
    PENDING = "Pending"
    SIGNED = "Signed"


class ContractUpdateData(TypedDict, total=False):
    total_amount: Decimal
    remaining_amount: Decimal


class Contract:
    def __init__(
        self,
        id: str,
        customer_id: str,
        commercial_id: str,
        created_by_id: str,
        total_amount: Decimal,
        remaining_amount: Decimal,
    ):
        self.id = id
        self.customer_id = customer_id
        self.commercial_id = commercial_id
        self.created_by_id = created_by_id
        self.total_amount = Decimal(total_amount)
        self.remaining_amount = Decimal(remaining_amount)
        self.status = ContractStatus.PENDING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.updated_by_id = None

    def update(self, data: ContractUpdateData, updater_id: str):
        for field, value in data.items():
            setattr(self, field, value)
        self.updated_at = datetime.now()
        self.updated_by_id = updater_id

    def sign_contract(self, updater_id: str):
        self.status = ContractStatus.SIGNED
        self.updated_at = datetime.now()
        self.updated_by_id = updater_id
