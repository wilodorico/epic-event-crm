import pytest

from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.collaborator import Collaborator, Role


@pytest.fixture
def manager():
    return Collaborator(
        id="manager-id",
        created_by_id="admin-id",
        first_name="Alice",
        last_name="Manager",
        email="alice.manager@test.com",
        password="securepassword",
        phone_number="1112223333",
        role=Role.MANAGEMENT,
    )


@pytest.fixture
def support_user():
    return Collaborator(
        id="support-id",
        created_by_id="admin-id",
        first_name="Bob",
        last_name="Support",
        email="bob.support@test.com",
        password="securepassword",
        phone_number="4445556666",
        role=Role.SUPPORT,
    )


@pytest.fixture
def marketing_user():
    return Collaborator(
        id="marketing-id",
        created_by_id="admin-id",
        first_name="Carol",
        last_name="Marketing",
        email="carol.marketing@test.com",
        password="securepassword",
        phone_number="7778889999",
        role=Role.MARKETING,
    )


def test_manager_can_create_collaborator(manager):
    auth_context = AuthContext(manager)
    assert auth_context.can_create_collaborator() is True

    auth_context.ensure_can_create_collaborator()


def test_support_cannot_create_collaborator(support_user):
    auth_context = AuthContext(support_user)
    assert auth_context.can_create_collaborator() is False

    with pytest.raises(PermissionError, match="Only managers can create collaborators"):
        auth_context.ensure_can_create_collaborator()


def test_marketing_cannot_create_collaborator(marketing_user):
    auth_context = AuthContext(marketing_user)
    assert auth_context.can_create_collaborator() is False

    with pytest.raises(PermissionError, match="Only managers can create collaborators"):
        auth_context.ensure_can_create_collaborator()
        auth_context.ensure_can_create_collaborator()
