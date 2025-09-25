import pytest
from click.testing import CliRunner

from collaborators.domain.contract.contract import Contract
from collaborators.infrastructure.cli.commands.contract import contract
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository


@pytest.fixture
def contract_to_update(john_commercial, karim_customer, manager_alice):
    return Contract(
        id="id-contract-to-update",
        customer_id=karim_customer.id,
        commercial_id=john_commercial.id,
        created_by_id=manager_alice.id,
        total_amount=1000.00,
        remaining_amount=1000.00,
    )


def test_manager_update_contract_success_cli(session, contract_to_update):
    repo = SqlalchemyContractRepository(session)
    repo.create(contract_to_update)

    user_input = (
        "id-contract-to-update\n"  # Contract ID prompt
        "1200.00\n"  # Total Amount prompt
        "1200.00\n"  # Remaining Amount prompt
    )

    runner = CliRunner()
    result = runner.invoke(
        contract,
        ["update-contract"],
        input=user_input,
        obj={"session": session},
    )

    assert result.exit_code == 0
    assert "Contract id-contract-to-update updated successfully" in result.output

    updated_contract = repo.find_by_id("id-contract-to-update")
    assert updated_contract is not None
    assert updated_contract.total_amount == 1200.00
    assert updated_contract.remaining_amount == 1200.00
