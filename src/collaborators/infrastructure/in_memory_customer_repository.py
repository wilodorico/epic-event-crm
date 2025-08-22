from collaborators.domain.customer.customer import Customer


class InMemoryCustomerRepository:
    def __init__(self):
        self.customers: dict[str, Customer] = {}

    def create(self, customer: Customer) -> None:
        self.customers[customer.id] = customer

    def find_by_email(self, email: str) -> Customer | None:
        return next((c for c in self.customers.values() if c.email == email), None)
