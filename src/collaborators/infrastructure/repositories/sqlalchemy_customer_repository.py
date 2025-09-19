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
        stmt = select(CustomerModel).where(CustomerModel.email == email)
        customer_model = self.session.execute(stmt).scalar_one_or_none()
        if customer_model:
            return CustomerMapper.to_entity(customer_model)
        return None
