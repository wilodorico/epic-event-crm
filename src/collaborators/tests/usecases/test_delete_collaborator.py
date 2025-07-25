import pytest

from collaborators.application.delete_collaborator_use_case import DeleteCollaboratorUseCase
from collaborators.application.services.auth_context import AuthContext


def test_manager_can_delete_collaborator_success(repository, manager_alice, fixed_id_generator, john_doe):
    auth_context = AuthContext(manager_alice)
    repository.create(john_doe)
    use_case = DeleteCollaboratorUseCase(repository, fixed_id_generator, auth_context)
    collaborator_to_delete = repository.find_by_id("john-marketing-1")
    use_case.execute(manager_alice, collaborator_to_delete.id)
    assert repository.find_by_id("john-marketing-1") is None


def test_non_manager_cannot_delete_collaborator(repository, fixed_id_generator, john_doe, bob_support):
    repository.create(john_doe)
    auth_context = AuthContext(bob_support)
    use_case = DeleteCollaboratorUseCase(repository, fixed_id_generator, auth_context)

    with pytest.raises(PermissionError, match="You do not have permission to perform this action."):
        use_case.execute(bob_support, john_doe.id)


def test_delete_non_existent_collaborator(repository, fixed_id_generator, manager_alice):
    auth_context = AuthContext(manager_alice)
    use_case = DeleteCollaboratorUseCase(repository, fixed_id_generator, auth_context)

    with pytest.raises(ValueError, match="Collaborator not found."):
        use_case.execute(manager_alice, "non-existent-id")
