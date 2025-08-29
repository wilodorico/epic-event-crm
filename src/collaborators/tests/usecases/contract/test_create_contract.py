import pytest

from collaborators.application.contract.create_contract_use_case import CreateContractUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.infrastructure.in_memory_contract_repository import InMemoryContractRepository
from collaborators.infrastructure.in_memory_customer_repository import InMemoryCustomerRepository


@pytest.fixture
def contract_data():
    return {
        "client_id": "karim-customer-1",
        "commercial_id": "commercial_123",
        "total_amount": 1000.00,
        "remaining_amount": 1000.00,
    }


def test_manager_can_create_contract(manager_alice, karim_customer, fixed_id_generator, contract_data):
    customer_repository = InMemoryCustomerRepository()
    customer_repository.create(karim_customer)

    auth_context = AuthContext(manager_alice)
    contract_repository = InMemoryContractRepository()
    use_case = CreateContractUseCase(customer_repository, contract_repository, fixed_id_generator, auth_context)

    contract = use_case.execute(creator=manager_alice, **contract_data)

    contract_db = contract_repository.find_by_id(contract.id)

    assert contract.id is not None
    assert contract_db.client_id == "karim-customer-1"
    assert contract_db.commercial_id == "commercial_123"
    assert contract_db.total_amount == 1000.00
    assert contract_db.remaining_amount == 1000.00
