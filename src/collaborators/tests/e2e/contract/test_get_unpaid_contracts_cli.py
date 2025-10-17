from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.contract import contract
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository


def test_commercial_can_get_contracts_unpaid_cli(
    session,
    john_commercial,
    karim_contract,
    karim_paid_contract,
):
    repo = SqlalchemyContractRepository(session)
    repo.create(karim_contract)
    repo.create(karim_paid_contract)

    runner = CliRunner()
    result = runner.invoke(
        contract,
        ["get-unpaid-contracts"],
        obj={"session": session, "current_user": john_commercial},
    )

    assert result.exit_code == 0
    assert "List of Unpaid Contracts:" in result.output
    assert karim_contract.id in result.output
    assert karim_paid_contract.id not in result.output
