import pytest

from collaborators.application.create_customer_use_case import CreateCustomerUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.infrastructure.in_memory_customer_repository import InMemoryCustomerRepository


@pytest.fixture
def tariq_customer():
    return {
        "first_name": "Tariq",
        "last_name": "Elam",
        "email": "tariq.elam@mail.com",
        "phone_number": "0601010101",
        "company": "TechCorp",
    }


def test_commercial_can_create_customer(john_commercial, fixed_id_generator, tariq_customer):
    auth_context = AuthContext(john_commercial)
    repository = InMemoryCustomerRepository()
    use_case = CreateCustomerUseCase(repository, fixed_id_generator, auth_context)
    use_case.execute(creator=john_commercial, **tariq_customer)

    customer = repository.find_by_email("tariq.elam@mail.com")
    assert customer is not None
    assert customer.first_name == "Tariq"
    assert customer.last_name == "Elam"
    assert customer.email == "tariq.elam@mail.com"
    assert customer.phone_number == "0601010101"
    assert customer.company == "TechCorp"
    assert customer.commercial_contact == john_commercial.id
