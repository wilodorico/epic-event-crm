from decimal import Decimal

import pytest

from collaborators.application.contract.create_contract_use_case import CreateContractUseCase
from collaborators.application.services.auth_context import AuthContext


@pytest.fixture
def contract_data():
    return {
        "customer_id": "karim-customer-1",
        "commercial_id": "commercial_123",
        "total_amount": Decimal("1000.00"),
        "remaining_amount": Decimal("1000.00"),
    }


def test_manager_can_create_contract(
    customer_repository, contract_repository, manager_alice, karim_customer, uuid_generator, contract_data
):
    customer_repository.create(karim_customer)

    auth_context = AuthContext(manager_alice)
    use_case = CreateContractUseCase(customer_repository, contract_repository, uuid_generator, auth_context)

    contract = use_case.execute(creator=manager_alice, **contract_data)

    contract_db = contract_repository.find_by_id(contract.id)

    assert contract.id is not None
    assert contract_db.customer_id == "karim-customer-1"
    assert contract_db.commercial_id == "commercial_123"
    assert contract_db.total_amount == 1000.00
    assert contract_db.remaining_amount == 1000.00


def test_manager_cannot_create_contract_non_existent_customer(
    customer_repository, contract_repository, manager_alice, uuid_generator
):
    auth_context = AuthContext(manager_alice)
    use_case = CreateContractUseCase(customer_repository, contract_repository, uuid_generator, auth_context)

    with pytest.raises(ValueError, match="Customer does not exist"):
        use_case.execute(
            creator=manager_alice,
            customer_id="non-existent-customer",
            commercial_id="commercial_123",
            total_amount=Decimal("1000.00"),
            remaining_amount=Decimal("1000.00"),
        )


def test_non_manager_cannot_create_contract(
    customer_repository, contract_repository, john_commercial, karim_customer, uuid_generator, contract_data
):
    customer_repository.create(karim_customer)

    auth_context = AuthContext(john_commercial)
    use_case = CreateContractUseCase(customer_repository, contract_repository, uuid_generator, auth_context)

    with pytest.raises(PermissionError, match="You do not have permission to perform this action."):
        use_case.execute(creator=john_commercial, **contract_data)
