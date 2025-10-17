import pytest
from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.contract import contract
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository


@pytest.mark.skip(reason="To be implemented")
def test_commercial_can_get_contracts_unpaid_cli(
    session,
    john_commercial,
    karim_contract,
    marie_contract,
):
    repo = SqlalchemyContractRepository(session)
    repo.create(karim_contract)
    repo.create(marie_contract)

    runner = CliRunner()
    result = runner.invoke(
        contract,
        ["get-unpaid-contracts"],
        obj={"session": session, "current_user": john_commercial},
    )

    assert result.exit_code == 0
    assert "List of Unpaid Contracts:" in result.output
    assert karim_contract.id in result.output
    assert marie_contract.id not in result.output
