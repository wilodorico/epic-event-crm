import pytest

from collaborators.application.services.auth_context import AuthContext
from collaborators.application.update_collaborator_use_case import UpdateCollaboratorUseCase
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.in_memory_collaborator_repository import InMemoryCollaboratorRepository
from commons.fixed_id_generator import FixedIdGenerator


@pytest.fixture
def fixed_id_generator():
    return FixedIdGenerator()


@pytest.fixture
def manager_alice():
    return Collaborator(
        id="creator-id",
        created_by_id="1",
        first_name="Alice",
        last_name="Smith",
        email="alice.smith@test.com",
        password="securepassword",
        phone_number="1112223333",
        role=Role.MANAGEMENT,
    )


@pytest.fixture
def john_doe():
    return Collaborator(
        id="john-id-1",
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        password="securepassword",
        phone_number="1234567890",
        role=Role.MARKETING,
        created_by_id="creator-id",
    )


def test_manager_can_update_collaborator_success(manager_alice, fixed_id_generator, john_doe):
    repository = InMemoryCollaboratorRepository()
    repository.create(john_doe)
    auth_context = AuthContext(manager_alice)
    use_case = UpdateCollaboratorUseCase(repository, fixed_id_generator, auth_context)
    collaborator_to_update = repository.find_by_id("john-id-1")
    updated_collaborator = use_case.execute(
        manager_alice, collaborator_to_update.id, {"first_name": "Johnny", "last_name": "Dep"}
    )
    assert updated_collaborator.first_name == "Johnny"
    assert updated_collaborator.last_name == "Dep"
    assert updated_collaborator.updated_by_id == manager_alice.id


def test_non_manager_cannot_update_collaborator(fixed_id_generator, john_doe):
    repository = InMemoryCollaboratorRepository()
    repository.create(john_doe)
    non_manager = Collaborator(
        id="non-manager-id",
        first_name="Bob",
        last_name="Builder",
        email="bob.builder@test.com",
        password="securepassword",
        phone_number="9876543210",
        role=Role.SUPPORT,
        created_by_id="creator-id",
    )
    auth_context = AuthContext(non_manager)
    use_case = UpdateCollaboratorUseCase(repository, fixed_id_generator, auth_context)

    with pytest.raises(PermissionError, match="You do not have permission to perform this action."):
        use_case.execute(non_manager, john_doe.id, {"first_name": "Robert", "last_name": "Builder"})


def test_update_non_existent_collaborator_raises_error(manager_alice, fixed_id_generator):
    repository = InMemoryCollaboratorRepository()
    auth_context = AuthContext(manager_alice)
    use_case = UpdateCollaboratorUseCase(repository, fixed_id_generator, auth_context)

    with pytest.raises(ValueError, match="Collaborator not found."):
        use_case.execute(manager_alice, "non-existent-id", {"first_name": "Ghost", "last_name": "Walker"})
