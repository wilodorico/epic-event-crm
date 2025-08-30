from decimal import Decimal

import pytest

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


def test_manager_cannot_update_non_existent_contract(manager_alice, fixed_id_generator):
    contract_repository = InMemoryContractRepository()
    auth_context = AuthContext(manager_alice)
    update_use_case = UpdateContractUseCase(contract_repository, auth_context)

    with pytest.raises(ValueError, match="Contract not found."):
        update_use_case.execute(
            updater=manager_alice,
            contract_id="non-existent-contract",
            data={
                "total_amount": Decimal("1200.00"),
                "remaining_amount": Decimal("1200.00"),
            },
        )


def test_commercial_can_update_contract_for_own_customer(
    manager_alice, john_commercial, karim_customer, fixed_id_generator
):
    customer_repository = InMemoryCustomerRepository()
    customer_repository.create(karim_customer)
    contract_repository = InMemoryContractRepository()
    auth_context_manager_alice = AuthContext(manager_alice)

    create_use_case = CreateContractUseCase(
        customer_repository, contract_repository, fixed_id_generator, auth_context_manager_alice
    )
    contract = create_use_case.execute(
        creator=manager_alice,
        customer_id=karim_customer.id,
        commercial_id=john_commercial.id,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("1000.00"),
    )

    auth_context_john_commercial = AuthContext(john_commercial)
    update_use_case = UpdateContractUseCase(contract_repository, auth_context_john_commercial)

    updated_contract = update_use_case.execute(
        updater=john_commercial,
        contract_id=contract.id,
        data={
            "total_amount": Decimal("1200.00"),
            "remaining_amount": Decimal("1200.00"),
        },
    )

    assert updated_contract.total_amount == Decimal("1200.00")
    assert updated_contract.remaining_amount == Decimal("1200.00")


def test_commercial_cannot_update_contract_for_other_customer(
    manager_alice, john_commercial, amel_commercial, karim_customer, fixed_id_generator
):
    customer_repository = InMemoryCustomerRepository()
    customer_repository.create(karim_customer)
    contract_repository = InMemoryContractRepository()
    auth_context_manager_alice = AuthContext(manager_alice)

    create_use_case = CreateContractUseCase(
        customer_repository, contract_repository, fixed_id_generator, auth_context_manager_alice
    )
    contract = create_use_case.execute(
        creator=manager_alice,
        customer_id=karim_customer.id,
        commercial_id=john_commercial.id,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("1000.00"),
    )

    auth_context_amel_commercial = AuthContext(amel_commercial)
    update_use_case = UpdateContractUseCase(contract_repository, auth_context_amel_commercial)

    with pytest.raises(PermissionError, match="Commercial can only update their own customers contracts"):
        update_use_case.execute(
            updater=amel_commercial,
            contract_id=contract.id,
            data={
                "total_amount": Decimal("1200.00"),
                "remaining_amount": Decimal("1200.00"),
            },
        )
