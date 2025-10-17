from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.contract import contract
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository


def test_commercial_can_get_contracts_unsigned_cli(
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
        ["get-unsigned-contracts"],
        obj={"session": session, "current_user": john_commercial},
    )

    assert result.exit_code == 0
    assert "List of Unsigned Contracts:" in result.output
    assert karim_contract.id in result.output
    assert marie_contract.id not in result.output
