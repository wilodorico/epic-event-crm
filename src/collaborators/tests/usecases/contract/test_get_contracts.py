import pytest

from collaborators.application.contract.get_contracts_use_case import GetContractsUseCase
from collaborators.application.services.auth_context import AuthContext


@pytest.mark.parametrize("collaborator_fixture", ["john_commercial", "manager_alice", "bob_support"])
def test_collaborator_can_get_contracts(
    contract_repository, karim_contract, marie_contract, request, collaborator_fixture
):
    contract_repository.create(karim_contract)
    contract_repository.create(marie_contract)

    collaborator = request.getfixturevalue(collaborator_fixture)
    auth_context = AuthContext(collaborator)

    use_case = GetContractsUseCase(contract_repository, auth_context)
    contracts = use_case.execute()

    assert contract_repository.count() == 2
    assert any(c.id == "karim-contract-1" for c in contracts)
    assert any(c.id == "marie-contract-1" for c in contracts)
