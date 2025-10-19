import pytest

from collaborators.application.contract.get_unpaid_contracts_use_case import GetUnpaidContractsUseCase
from collaborators.application.services.auth_context import AuthContext


def test_commercial_can_get_unpaid_contracts(
    contract_repository, karim_contract, karim_paid_contract, john_commercial
):
    contract_repository.create(karim_contract)
    contract_repository.create(karim_paid_contract)

    auth_context = AuthContext(john_commercial)

    use_case = GetUnpaidContractsUseCase(auth_context, contract_repository)
    unpaid_contracts = use_case.execute(john_commercial.id)
    print("unpaid_contracts", unpaid_contracts)

    assert contract_repository.count() == 2
    assert len(unpaid_contracts) == 1
    assert any(c.id == "karim-contract-1" for c in unpaid_contracts)
    assert not any(c.id == "karim-contract-2" for c in unpaid_contracts)


def test_non_commercial_cannot_get_unpaid_contracts(contract_repository, bob_support):
    auth_context = AuthContext(bob_support)
    use_case = GetUnpaidContractsUseCase(auth_context, contract_repository)

    with pytest.raises(
        PermissionError,
        match=f"User '{bob_support.email}' with role 'Support' does not have permission 'FILTER_CONTRACTS'",
    ):
        use_case.execute(bob_support.id)
