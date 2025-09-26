import pytest
from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.contract import contract
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository


@pytest.mark.parametrize("collaborator_fixture", ["john_commercial", "manager_alice", "bob_support"])
def test_collaborator_can_get_contracts_cli(session, collaborator_fixture, karim_contract, marie_contract, request):
    repo = SqlalchemyContractRepository(session)
    repo.create(karim_contract)
    repo.create(marie_contract)

    collaborator = request.getfixturevalue(collaborator_fixture)

    runner = CliRunner()
    result = runner.invoke(
        contract,
        ["get-contracts"],
        obj={"session": session, "current_user": collaborator},
    )

    assert result.exit_code == 0
    assert "List of Contracts:" in result.output
    assert karim_contract.id in result.output
    assert marie_contract.id in result.output
    assert str(karim_contract.total_amount) in result.output
    assert str(marie_contract.total_amount) in result.output
