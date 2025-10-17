from sqlalchemy import select
from sqlalchemy.orm import Session

from collaborators.domain.customer.customer import Customer
from collaborators.infrastructure.database.models.customer import CustomerModel
from collaborators.infrastructure.mappers.customer import CustomerMapper


class SqlalchemyCustomerRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, customer: Customer) -> None:
        model = CustomerMapper.to_model(customer)
        self.session.add(model)
        self.session.commit()

    def find_by_email(self, email: str) -> Customer | None:
        query = select(CustomerModel).where(CustomerModel.email == email)
        customer_model = self.session.execute(query).scalar_one_or_none()
        if customer_model:
            return CustomerMapper.to_entity(customer_model)
        return None

    def find_by_id(self, customer_id: str) -> Customer | None:
        query = select(CustomerModel).where(CustomerModel.id == customer_id)
        customer_model = self.session.execute(query).scalar_one_or_none()
        if customer_model:
            return CustomerMapper.to_entity(customer_model)
        return None

    def update(self, customer: Customer) -> None:
        """Update an existing customer."""
        model = CustomerMapper.to_model(customer)
        # Merge updates the existing record with the same primary key
        self.session.merge(model)
        self.session.commit()

    def count(self) -> int:
        """Count all customers in the database."""
        query = select(CustomerModel)
        result = self.session.execute(query)
        return len(result.scalars().all())

    def get_all(self) -> list[Customer]:
        """Retrieve all customers from the database."""
        query = select(CustomerModel)
        result = self.session.execute(query)
        customer_models = result.scalars().all()
        return [CustomerMapper.to_entity(model) for model in customer_models]
