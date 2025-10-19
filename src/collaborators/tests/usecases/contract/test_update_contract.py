from decimal import Decimal

import pytest

from collaborators.application.contract.create_contract_use_case import CreateContractUseCase
from collaborators.application.contract.update_contract_use_case import UpdateContractUseCase
from collaborators.application.services.auth_context import AuthContext


def test_manager_can_update_contract(
    customer_repository, contract_repository, manager_alice, karim_customer, uuid_generator
):
    customer_repository.create(karim_customer)
    auth_context = AuthContext(manager_alice)

    create_use_case = CreateContractUseCase(auth_context, customer_repository, contract_repository, uuid_generator)
    contract = create_use_case.execute(
        creator=manager_alice,
        customer_id=karim_customer.id,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("1000.00"),
    )

    update_use_case = UpdateContractUseCase(auth_context, contract_repository)

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


def test_manager_cannot_update_non_existent_contract(contract_repository, manager_alice):
    auth_context = AuthContext(manager_alice)
    update_use_case = UpdateContractUseCase(auth_context, contract_repository)

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
    customer_repository, contract_repository, manager_alice, john_commercial, karim_customer, uuid_generator
):
    customer_repository.create(karim_customer)
    auth_context_manager_alice = AuthContext(manager_alice)

    create_use_case = CreateContractUseCase(
        auth_context_manager_alice, customer_repository, contract_repository, uuid_generator
    )
    contract = create_use_case.execute(
        creator=manager_alice,
        customer_id=karim_customer.id,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("1000.00"),
    )

    auth_context_john_commercial = AuthContext(john_commercial)
    update_use_case = UpdateContractUseCase(auth_context_john_commercial, contract_repository)

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
    customer_repository,
    contract_repository,
    manager_alice,
    amel_commercial,
    karim_customer,
    uuid_generator,
):
    customer_repository.create(karim_customer)
    auth_context_manager_alice = AuthContext(manager_alice)

    create_use_case = CreateContractUseCase(
        auth_context_manager_alice, customer_repository, contract_repository, uuid_generator
    )
    contract = create_use_case.execute(
        creator=manager_alice,
        customer_id=karim_customer.id,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("1000.00"),
    )

    auth_context_amel_commercial = AuthContext(amel_commercial)
    update_use_case = UpdateContractUseCase(auth_context_amel_commercial, contract_repository)

    with pytest.raises(PermissionError, match="Commercial can only update their own customers contracts"):
        update_use_case.execute(
            updater=amel_commercial,
            contract_id=contract.id,
            data={
                "total_amount": Decimal("1200.00"),
                "remaining_amount": Decimal("1200.00"),
            },
        )
