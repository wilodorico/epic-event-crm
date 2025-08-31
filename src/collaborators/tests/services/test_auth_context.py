import pytest

from collaborators.application.exceptions.authorization_error import AuthorizationError
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.permissions import Permissions


@pytest.mark.parametrize(
    "permission",
    [
        Permissions.CREATE_COLLABORATOR,
        Permissions.UPDATE_COLLABORATOR,
        Permissions.DELETE_COLLABORATOR,
    ],
)
def test_manager_can_create_collaborator(manager_alice, permission):
    auth_context = AuthContext(manager_alice)
    assert auth_context.can(permission) is True

    auth_context.ensure(permission)


@pytest.mark.parametrize(
    "permission",
    [
        Permissions.CREATE_COLLABORATOR,
        Permissions.UPDATE_COLLABORATOR,
        Permissions.DELETE_COLLABORATOR,
    ],
)
def test_support_cannot_create_collaborator(bob_support, permission):
    auth_context = AuthContext(bob_support)
    assert auth_context.can(permission) is False

    with pytest.raises(AuthorizationError) as exc_info:
        auth_context.ensure(permission)

    assert bob_support.email in str(exc_info.value)


@pytest.mark.parametrize(
    "permission",
    [
        Permissions.CREATE_COLLABORATOR,
        Permissions.UPDATE_COLLABORATOR,
        Permissions.DELETE_COLLABORATOR,
    ],
)
def test_marketing_cannot_create_collaborator(john_commercial, permission):
    auth_context = AuthContext(john_commercial)
    assert auth_context.can(permission) is False

    with pytest.raises(AuthorizationError) as exc_info:
        auth_context.ensure(permission)

    assert john_commercial.email in str(exc_info.value)
