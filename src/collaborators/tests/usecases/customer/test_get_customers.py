import pytest

from collaborators.application.customer.get_customers_use_case import GetCustomersUseCase
from collaborators.application.services.auth_context import AuthContext


@pytest.mark.parametrize("collaborator_fixture", ["john_commercial", "manager_alice", "bob_support"])
def test_all_collaborator_roles_can_get_customers(
    customer_repository, karim_customer, marie_customer, request, collaborator_fixture
):
    customer_repository.create(karim_customer)
    customer_repository.create(marie_customer)

    collaborator = request.getfixturevalue(collaborator_fixture)
    auth_context = AuthContext(collaborator)

    use_case = GetCustomersUseCase(auth_context, customer_repository)
    customers = use_case.execute()

    assert customer_repository.count() == 2
    assert any(c.first_name == "Karim" for c in customers)
    assert any(c.first_name == "Marie" for c in customers)


@pytest.mark.parametrize("collaborator_fixture", ["john_commercial", "manager_alice", "bob_support"])
def test_all_collaborator_get_customers_empty_repository(customer_repository, request, collaborator_fixture):
    auth_context = AuthContext(request.getfixturevalue(collaborator_fixture))
    use_case = GetCustomersUseCase(auth_context, customer_repository)

    customers = use_case.execute()

    assert customer_repository.count() == 0
    assert customers == []
