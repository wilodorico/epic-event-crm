import pytest

from collaborators.application.customer.create_customer_use_case import CreateCustomerUseCase
from collaborators.application.customer.update_customer_use_case import UpdateCustomerUseCase
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


def test_commercial_can_update_own_customer(customer_repository, john_commercial, uuid_generator, tariq_customer):
    auth_context = AuthContext(john_commercial)
    create_use_case = CreateCustomerUseCase(customer_repository, uuid_generator, auth_context)
    customer = create_use_case.execute(creator=john_commercial, **tariq_customer)

    update_use_case = UpdateCustomerUseCase(customer_repository, auth_context)
    updated_customer = update_use_case.execute(
        updater=john_commercial,
        customer_id=customer.id,
        data={"last_name": "Elamir"},
    )
    assert updated_customer.last_name == "Elamir"
    assert updated_customer.first_name == "Tariq"


def test_commercial_cannot_update_other_customer(
    customer_repository,
    jane_commercial,
    john_commercial,
    uuid_generator,
    tariq_customer,
):
    auth_context = AuthContext(jane_commercial)
    create_use_case = CreateCustomerUseCase(customer_repository, uuid_generator, auth_context)
    customer = create_use_case.execute(creator=john_commercial, **tariq_customer)

    update_use_case = UpdateCustomerUseCase(customer_repository, auth_context)

    with pytest.raises(PermissionError):
        update_use_case.execute(
            updater=jane_commercial,
            customer_id=customer.id,
            data={"last_name": "Elamir"},
        )


def test_update_customer_not_found(customer_repository, john_commercial):
    auth_context = AuthContext(john_commercial)
    update_use_case = UpdateCustomerUseCase(customer_repository, auth_context)

    with pytest.raises(ValueError, match="Customer not found."):
        update_use_case.execute(
            updater=john_commercial,
            customer_id="non-existent-id",
            data={"last_name": "Elamir"},
        )
    update_use_case = UpdateCustomerUseCase(customer_repository, auth_context)

    with pytest.raises(ValueError, match="Customer not found."):
        update_use_case.execute(
            updater=john_commercial,
            customer_id="non-existent-id",
            data={"last_name": "Elamir"},
        )
