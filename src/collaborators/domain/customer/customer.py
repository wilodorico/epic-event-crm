from datetime import datetime
from typing import TypedDict


class CustomerUpdateData(TypedDict, total=False):
    """Typed dictionary for updating customer data.

    Used to pass partial updates to a `Customer` instance.
    All fields are optional.
    """

    first_name: str
    last_name: str
    email: str
    phone_number: str
    company: str


class CustomerContactInfo(TypedDict):
    """Typed dictionary for customer contact information.

    Contains the essential contact details for a customer.
    All fields are required.
    """

    email: str
    phone_number: str


class Customer:
    """Domain entity representing a customer in the CRM system.

    A customer is a client managed by a commercial contact. This entity tracks personal
    and company information, contact details, and the assigned commercial representative
    responsible for managing the relationship and contracts.
    """

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
        """Updates the customer's data with the provided fields.

        Args:
            data: Fields to update (as `CustomerUpdateData`).

        Note:
            Updates `updated_at` on success.
        """
        for field, value in data.items():
            setattr(self, field, value)
        self.updated_at = datetime.now()

    def get_contact_info(self) -> CustomerContactInfo:
        """Retrieves the customer's contact information.

        Returns:
            CustomerContactInfo: A dictionary containing the email and phone number.
        """
        return {
            "email": self.email,
            "phone_number": self.phone_number,
        }
