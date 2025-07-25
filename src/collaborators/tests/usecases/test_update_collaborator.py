import pytest

from collaborators.application.services.auth_context import AuthContext
from collaborators.application.update_collaborator_use_case import UpdateCollaboratorUseCase
from collaborators.domain.collaborator.collaborator import Role


def test_manager_can_update_collaborator_partial_success(
    repository, manager_alice, fixed_id_generator, john_marketing
):
    repository.create(john_marketing)
    auth_context = AuthContext(manager_alice)
    use_case = UpdateCollaboratorUseCase(repository, fixed_id_generator, auth_context)
    collaborator_to_update = repository.find_by_id("john-marketing-1")
    updated_collaborator = use_case.execute(
        manager_alice, collaborator_to_update.id, {"first_name": "Johnny", "last_name": "Dep"}
    )
    assert updated_collaborator.first_name == "Johnny"
    assert updated_collaborator.last_name == "Dep"
    assert updated_collaborator.updated_by_id == manager_alice.id


def test_manager_can_update_collaborator_full_success(repository, manager_alice, fixed_id_generator, john_marketing):
    repository.create(john_marketing)
    auth_context = AuthContext(manager_alice)
    use_case = UpdateCollaboratorUseCase(repository, fixed_id_generator, auth_context)
    collaborator_to_update = repository.find_by_id("john-marketing-1")
    updated_collaborator = use_case.execute(
        manager_alice,
        collaborator_to_update.id,
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@gmail.com",
            "phone_number": "1234567890",
            "role": Role.MARKETING,
        },
    )
    assert updated_collaborator.first_name == "John"
    assert updated_collaborator.last_name == "Doe"
    assert updated_collaborator.email == "john.doe@gmail.com"
    assert updated_collaborator.phone_number == "1234567890"
    assert updated_collaborator.role == Role.MARKETING
    assert updated_collaborator.updated_by_id == manager_alice.id


def test_non_manager_cannot_update_collaborator(repository, fixed_id_generator, john_marketing, bob_support):
    repository.create(john_marketing)
    auth_context = AuthContext(bob_support)
    use_case = UpdateCollaboratorUseCase(repository, fixed_id_generator, auth_context)

    with pytest.raises(PermissionError, match="You do not have permission to perform this action."):
        use_case.execute(bob_support, john_marketing.id, {"first_name": "Robert", "last_name": "Builder"})


def test_update_non_existent_collaborator_raises_error(repository, fixed_id_generator, manager_alice):
    auth_context = AuthContext(manager_alice)
    use_case = UpdateCollaboratorUseCase(repository, fixed_id_generator, auth_context)

    with pytest.raises(ValueError, match="Collaborator not found."):
        use_case.execute(manager_alice, "non-existent-id", {"first_name": "Ghost", "last_name": "Walker"})
