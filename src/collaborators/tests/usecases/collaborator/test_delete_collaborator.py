import pytest

from collaborators.application.collaborator.delete_collaborator_use_case import DeleteCollaboratorUseCase
from collaborators.application.exceptions.authorization_error import AuthorizationError
from collaborators.application.services.auth_context import AuthContext


def test_manager_can_delete_collaborator_success(
    collaborator_repository, manager_alice, uuid_generator, john_commercial
):
    auth_context = AuthContext(manager_alice)
    collaborator_repository.create(john_commercial)
    use_case = DeleteCollaboratorUseCase(auth_context, collaborator_repository, uuid_generator)
    collaborator_to_delete = collaborator_repository.find_by_id(john_commercial.id)
    use_case.execute(collaborator_to_delete.id)
    assert collaborator_repository.find_by_id(john_commercial.id) is None


def test_non_manager_cannot_delete_collaborator(collaborator_repository, uuid_generator, john_commercial, bob_support):
    collaborator_repository.create(john_commercial)
    auth_context = AuthContext(bob_support)
    use_case = DeleteCollaboratorUseCase(auth_context, collaborator_repository, uuid_generator)

    with pytest.raises(AuthorizationError) as exc_info:
        use_case.execute(john_commercial.id)

    assert bob_support.email in str(exc_info.value)


def test_delete_non_existent_collaborator(collaborator_repository, uuid_generator, manager_alice):
    auth_context = AuthContext(manager_alice)
    use_case = DeleteCollaboratorUseCase(auth_context, collaborator_repository, uuid_generator)

    with pytest.raises(ValueError, match="Collaborator not found."):
        use_case.execute("non-existent-id")
