import pytest

from collaborators.application.contract.sign_contract_use_case import SignContractUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.contract.contract import ContractStatus


@pytest.mark.parametrize("collaborator_fixture", ["john_commercial", "manager_alice"])
def test_collaborator_can_sign_contract(
    contract_repository, karim_contract, manager_alice, request, collaborator_fixture
):
    contract_repository.create(karim_contract)
    collaborator = request.getfixturevalue(collaborator_fixture)

    auth_context = AuthContext(collaborator)

    use_case = SignContractUseCase(auth_context, contract_repository)

    use_case.execute(updater_id=manager_alice.id, contract_id=karim_contract.id)

    signed_contract = contract_repository.find_by_id(karim_contract.id)
    assert signed_contract is not None
    assert signed_contract.status == ContractStatus.SIGNED


def test_support_cannot_sign_contract(contract_repository, karim_contract, bob_support):
    contract_repository.create(karim_contract)
    auth_context = AuthContext(bob_support)

    use_case = SignContractUseCase(auth_context, contract_repository)

    with pytest.raises(PermissionError) as exc_info:
        use_case.execute(updater_id=bob_support.id, contract_id=karim_contract.id)

    assert f"User '{bob_support.email}' with role 'Support' does not have permission" in str(exc_info.value)

    unsigned_contract = contract_repository.find_by_id(karim_contract.id)
    assert unsigned_contract is not None
    assert unsigned_contract.status == ContractStatus.PENDING


def test_manager_cannot_sign_non_existent_contract(contract_repository, manager_alice):
    auth_context = AuthContext(manager_alice)

    use_case = SignContractUseCase(auth_context, contract_repository)

    with pytest.raises(ValueError) as exc_info:
        use_case.execute(updater_id=manager_alice.id, contract_id="non-existent-id")

    assert "Contract not found." in str(exc_info.value)
    assert contract_repository.count() == 0
