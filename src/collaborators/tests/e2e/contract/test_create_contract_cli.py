from decimal import Decimal

import pytest
from click.testing import CliRunner

from collaborators.domain.customer.customer import Customer
from collaborators.infrastructure.cli.commands.contract import contract
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository
from collaborators.infrastructure.repositories.sqlalchemy_customer_repository import SqlalchemyCustomerRepository


@pytest.fixture
def alice_customer(john_commercial):
    return Customer(
        id="id-alice-customer",
        first_name="Alice",
        last_name="Wonderland",
        email="alice.wonderland@test.com",
        phone_number="1234567890",
        company="Wonderland Inc.",
        commercial_contact_id=john_commercial.id,
    )


def test_manager_create_contract_success_cli(session, alice_customer, john_commercial, manager_alice):
    customer_repo = SqlalchemyCustomerRepository(session)
    contract_repo = SqlalchemyContractRepository(session)
    customer_repo.create(alice_customer)

    user_input = (
        f"{alice_customer.id}\n"  # --customer-id
        "1000.00\n"  # --total-amount
        "1000.00\n"  # --remaining-amount
    )

    runner = CliRunner()
    result = runner.invoke(
        contract, ["create-contract"], input=user_input, obj={"session": session, "current_user": manager_alice}
    )

    assert result.exit_code == 0
    customer_contracts = contract_repo.find_by_customer_id(alice_customer.id)
    created_contract = customer_contracts[0]

    assert f"✅ Contract {created_contract.id} created successfully" in result.output
    assert created_contract.commercial_id == john_commercial.id
    assert created_contract.customer_id == alice_customer.id
    assert Decimal(created_contract.total_amount) == 1000.00
    assert Decimal(created_contract.remaining_amount) == 1000.00
    assert created_contract.status.name == "PENDING"


def test_manager_create_contract_non_existent_customer_cli(session, manager_alice):
    user_input = (
        "non-existent-customer-id\n"  # --customer-id
        "1000.00\n"  # --total-amount
        "1000.00\n"  # --remaining-amount
    )

    runner = CliRunner()
    result = runner.invoke(
        contract, ["create-contract"], input=user_input, obj={"session": session, "current_user": manager_alice}
    )

    assert result.exit_code == 1
    assert "❌ Error creating contract: Customer does not exist" in result.output


def test_manager_create_contract_with_negative_total_amount_cli(session, alice_customer, manager_alice):
    customer_repo = SqlalchemyCustomerRepository(session)
    contract_repo = SqlalchemyContractRepository(session)
    customer_repo.create(alice_customer)

    user_input = (
        f"{alice_customer.id}\n"  # --customer-id
        "-1000.00\n"  # Invalid --total-amount
        "1000.00\n"  # --remaining-amount
    )

    runner = CliRunner()
    result = runner.invoke(
        contract, ["create-contract"], input=user_input, obj={"session": session, "current_user": manager_alice}
    )

    assert result.exit_code == 1
    assert "Error: Value must be a positive decimal number" in result.output
    customer_contracts = contract_repo.find_by_customer_id(alice_customer.id)
    assert len(customer_contracts) == 0


def test_manager_create_contract_with_non_numeric_total_amount_cli(session, alice_customer, manager_alice):
    customer_repo = SqlalchemyCustomerRepository(session)
    contract_repo = SqlalchemyContractRepository(session)
    customer_repo.create(alice_customer)

    user_input = (
        f"{alice_customer.id}\n"  # --customer-id
        "abc\n"  # Invalid --total-amount
        "1000.00\n"  # --remaining-amount
    )

    runner = CliRunner()
    result = runner.invoke(
        contract, ["create-contract"], input=user_input, obj={"session": session, "current_user": manager_alice}
    )

    assert result.exit_code == 1
    assert "Error: Value must be a valid decimal number" in result.output
    customer_contracts = contract_repo.find_by_customer_id(alice_customer.id)
    assert len(customer_contracts) == 0


def test_non_manager_cannot_create_contract_cli(session, alice_customer, john_commercial):
    customer_repo = SqlalchemyCustomerRepository(session)
    contract_repo = SqlalchemyContractRepository(session)
    customer_repo.create(alice_customer)

    user_input = (
        f"{alice_customer.id}\n"  # --customer-id
        "1000.00\n"  # --total-amount
        "1000.00\n"  # --remaining-amount
    )

    runner = CliRunner()
    result = runner.invoke(
        contract, ["create-contract"], input=user_input, obj={"session": session, "current_user": john_commercial}
    )

    assert result.exit_code == 1
    assert (
        "❌ Error creating contract: User 'john.doe@test.com' with role 'Commercial' does not have permission"
        in result.output
    )
    customer_contracts = contract_repo.find_by_customer_id(alice_customer.id)
    assert len(customer_contracts) == 0
