import pytest

from collaborators.application.collaborator.delete_collaborator_use_case import DeleteCollaboratorUseCase
from collaborators.application.services.auth_context import AuthContext


def test_manager_can_delete_collaborator_success(
    collaborator_repository, manager_alice, uuid_generator, john_commercial
):
    auth_context = AuthContext(manager_alice)
    collaborator_repository.create(john_commercial)
    use_case = DeleteCollaboratorUseCase(collaborator_repository, uuid_generator, auth_context)
    collaborator_to_delete = collaborator_repository.find_by_id(john_commercial.id)
    use_case.execute(manager_alice, collaborator_to_delete.id)
    assert collaborator_repository.find_by_id(john_commercial.id) is None


def test_non_manager_cannot_delete_collaborator(collaborator_repository, uuid_generator, john_commercial, bob_support):
    collaborator_repository.create(john_commercial)
    auth_context = AuthContext(bob_support)
    use_case = DeleteCollaboratorUseCase(collaborator_repository, uuid_generator, auth_context)

    with pytest.raises(PermissionError, match="You do not have permission to perform this action."):
        use_case.execute(bob_support, john_commercial.id)


def test_delete_non_existent_collaborator(collaborator_repository, uuid_generator, manager_alice):
    auth_context = AuthContext(manager_alice)
    use_case = DeleteCollaboratorUseCase(collaborator_repository, uuid_generator, auth_context)

    with pytest.raises(ValueError, match="Collaborator not found."):
        use_case.execute(manager_alice, "non-existent-id")
