from collaborators.domain.customer.customer import Customer


class InMemoryCustomerRepository:
    def __init__(self):
        self.customers: dict[str, Customer] = {}

    def create(self, customer: Customer) -> None:
        self.customers[customer.id] = customer

    def find_by_email(self, email: str) -> Customer | None:
        return next((c for c in self.customers.values() if c.email == email), None)

    def find_by_id(self, customer_id: str) -> Customer | None:
        return self.customers.get(customer_id)

    def update(self, customer: Customer) -> None:
        self.customers[customer.id] = customer

    def count(self) -> int:
        """Count all customers in memory."""
        return len(self.customers)

    def get_all(self) -> list[Customer] | list:
        """Retrieve all customers from memory."""
        return list(self.customers.values())
