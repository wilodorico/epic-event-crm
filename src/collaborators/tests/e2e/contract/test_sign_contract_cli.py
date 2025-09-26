import pytest
from click.testing import CliRunner

from collaborators.domain.contract.contract import ContractStatus
from collaborators.infrastructure.cli.commands.contract import contract
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository


@pytest.mark.parametrize("collaborator_fixture", ["john_commercial", "manager_alice"])
def test_collaborator_can_sign_contract_cli(session, karim_contract, collaborator_fixture, request):
    repo = SqlalchemyContractRepository(session)
    repo.create(karim_contract)

    collaborator = request.getfixturevalue(collaborator_fixture)

    user_input = "yes\n"  # Confirm signing prompt

    runner = CliRunner()
    result = runner.invoke(
        contract,
        ["sign-contract", "--id", karim_contract.id],
        input=user_input,
        obj={"session": session, "current_user": collaborator},
    )

    assert result.exit_code == 0
    assert f"Contract with ID '{karim_contract.id}' has been signed successfully." in result.output

    signed_contract = repo.find_by_id(karim_contract.id)
    assert signed_contract is not None
    assert signed_contract.status == ContractStatus.SIGNED
