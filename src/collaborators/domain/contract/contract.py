from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TypedDict


class ContractStatus(Enum):
    """Enumeration of possible contract statuses."""

    PENDING = "Pending"
    SIGNED = "Signed"


class ContractUpdateData(TypedDict, total=False):
    """Typed dictionary for updating contract data.

    Used to pass partial updates to a `Contract` instance.
    All fields are optional.
    """

    total_amount: Decimal
    remaining_amount: Decimal


class Contract:
    """Domain entity representing a contract between a customer and the company.

    A contract tracks the financial agreement for services, including total and remaining
    amounts, signature status, and the commercial contact responsible. Contracts must be
    signed before events can be created and link customers to their commercial representatives.
    """

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
        """Updates the contract's data with the provided fields.

        Args:
            data: Fields to update (as `ContractUpdateData`).
            updater_id: ID of the user performing the update.

        Note:
            Updates `updated_at` and `updated_by_id` on success.
        """
        for field, value in data.items():
            setattr(self, field, value)
        self.updated_at = datetime.now()
        self.updated_by_id = updater_id

    def sign_contract(self, updater_id: str):
        """Signs the contract and updates its status to SIGNED.

        Args:
            updater_id: ID of the user signing the contract.

        Note:
            Updates `status`, `updated_at`, and `updated_by_id` on success.
        """
        self.status = ContractStatus.SIGNED
        self.updated_at = datetime.now()
        self.updated_by_id = updater_id

    def is_signed(self) -> bool:
        """Checks if the contract has been signed.

        Returns:
            bool: True if the contract status is SIGNED, False otherwise.
        """
        return self.status == ContractStatus.SIGNED

    def is_paid(self) -> bool:
        """Checks if the contract has been fully paid.

        Returns:
            bool: True if the remaining amount is zero, False otherwise.
        """
        return self.remaining_amount == Decimal("0.00")
