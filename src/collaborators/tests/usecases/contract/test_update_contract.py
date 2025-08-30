from decimal import Decimal

from collaborators.application.contract.create_contract_use_case import CreateContractUseCase
from collaborators.application.contract.update_contract_use_case import UpdateContractUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.infrastructure.in_memory_contract_repository import InMemoryContractRepository
from collaborators.infrastructure.in_memory_customer_repository import InMemoryCustomerRepository


def test_manager_can_update_contract(manager_alice, john_commercial, karim_customer, fixed_id_generator):
    customer_repository = InMemoryCustomerRepository()
    customer_repository.create(karim_customer)
    contract_repository = InMemoryContractRepository()
    auth_context = AuthContext(manager_alice)

    create_use_case = CreateContractUseCase(customer_repository, contract_repository, fixed_id_generator, auth_context)
    contract = create_use_case.execute(
        creator=manager_alice,
        customer_id=karim_customer.id,
        commercial_id=john_commercial.id,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("1000.00"),
    )

    update_use_case = UpdateContractUseCase(contract_repository, auth_context)

    updated_contract = update_use_case.execute(
        updater=manager_alice,
        contract_id=contract.id,
        data={
            "total_amount": Decimal("1200.00"),
            "remaining_amount": Decimal("1200.00"),
        },
    )

    assert updated_contract.total_amount == Decimal("1200.00")
    assert updated_contract.remaining_amount == Decimal("1200.00")
