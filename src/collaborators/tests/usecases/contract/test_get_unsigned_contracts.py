import pytest

from collaborators.application.contract.get_unsigned_contracts_use_case import GetUnsignedContractsUseCase
from collaborators.application.services.auth_context import AuthContext


def test_commercial_can_get_unsigned_contracts(contract_repository, karim_contract, marie_contract, john_commercial):
    contract_repository.create(karim_contract)
    contract_repository.create(marie_contract)

    auth_context = AuthContext(john_commercial)

    use_case = GetUnsignedContractsUseCase(contract_repository, auth_context)
    unsigned_contracts = use_case.execute(john_commercial.id)
    print("unsigned_contracts", unsigned_contracts)

    assert contract_repository.count() == 2
    assert len(unsigned_contracts) == 1
    assert any(c.id == "karim-contract-1" for c in unsigned_contracts)
    assert not any(c.id == "marie-contract-1" for c in unsigned_contracts)


def test_non_commercial_cannot_get_unsigned_contracts(contract_repository, bob_support):
    auth_context = AuthContext(bob_support)
    use_case = GetUnsignedContractsUseCase(contract_repository, auth_context)

    with pytest.raises(
        PermissionError,
        match=f"User '{bob_support.email}' with role 'Support' does not have permission 'FILTER_CONTRACTS'",
    ):
        use_case.execute(bob_support.id)
