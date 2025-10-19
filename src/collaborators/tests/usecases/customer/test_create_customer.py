import pytest

from collaborators.application.customer.create_customer_use_case import CreateCustomerUseCase
from collaborators.application.exceptions.authorization_error import AuthorizationError
from collaborators.application.services.auth_context import AuthContext


@pytest.fixture
def tariq_customer():
    return {
        "first_name": "Tariq",
        "last_name": "Elam",
        "email": "tariq.elam@mail.com",
        "phone_number": "0601010101",
        "company": "TechCorp",
    }


def test_commercial_can_create_customer(customer_repository, john_commercial, uuid_generator, tariq_customer):
    auth_context = AuthContext(john_commercial)
    use_case = CreateCustomerUseCase(auth_context, customer_repository, uuid_generator)
    created_customer = use_case.execute(creator=john_commercial, **tariq_customer)

    customer = customer_repository.find_by_email(created_customer.email)
    assert customer.id is not None
    assert customer.first_name == "Tariq"
    assert customer.last_name == "Elam"
    assert customer.email == "tariq.elam@mail.com"
    assert customer.phone_number == "0601010101"
    assert customer.company == "TechCorp"
    assert customer.commercial_contact_id == john_commercial.id


def test_commercial_cannot_create_customer_with_existing_email(
    customer_repository, john_commercial, uuid_generator, tariq_customer
):
    auth_context = AuthContext(john_commercial)
    use_case = CreateCustomerUseCase(auth_context, customer_repository, uuid_generator)

    use_case.execute(creator=john_commercial, **tariq_customer)

    with pytest.raises(ValueError, match="Email already exists"):
        use_case.execute(creator=john_commercial, **tariq_customer)


def test_non_commercial_cannot_create_customer(customer_repository, manager_alice, uuid_generator, tariq_customer):
    auth_context = AuthContext(manager_alice)
    use_case = CreateCustomerUseCase(auth_context, customer_repository, uuid_generator)

    with pytest.raises(AuthorizationError) as exc_info:
        use_case.execute(creator=manager_alice, **tariq_customer)

    assert manager_alice.email in str(exc_info.value)
