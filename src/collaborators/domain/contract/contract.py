from datetime import datetime
from decimal import Decimal
from enum import Enum


class ContractStatus(Enum):
    PENDING = "Pending"
    SIGNED = "Signed"


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
