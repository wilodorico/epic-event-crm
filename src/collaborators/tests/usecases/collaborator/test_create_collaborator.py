import pytest

from collaborators.application.collaborator.create_collaborator_use_case import CreateCollaboratorUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.collaborator import Role


@pytest.fixture
def data_john_doe():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "password": "securepassword",
        "phone_number": "1234567890",
        "role": Role.COMMERCIAL,
    }


def test_manager_can_create_collaborator(collaborator_repository, data_john_doe, manager_alice, uuid_generator):
    auth_context = AuthContext(manager_alice)
    use_case = CreateCollaboratorUseCase(collaborator_repository, uuid_generator, auth_context)
    use_case.execute(creator=manager_alice, **data_john_doe)

    collaborator = collaborator_repository.find_by_email(data_john_doe["email"])

    assert len(collaborator_repository.collaborators) == 1
    assert collaborator.id is not None
    assert collaborator.first_name == "John"
    assert collaborator.last_name == "Doe"
    assert collaborator.email == "john.doe@test.com"
    assert collaborator.phone_number == "1234567890"
    assert collaborator.role == Role.COMMERCIAL


def test_manager_cannot_create_collaborator_with_existing_email(
    collaborator_repository, data_john_doe, manager_alice, uuid_generator
):
    auth_context = AuthContext(manager_alice)
    use_case = CreateCollaboratorUseCase(collaborator_repository, uuid_generator, auth_context)
    use_case.execute(creator=manager_alice, **data_john_doe)
    existing_email = data_john_doe["email"]

    with pytest.raises(ValueError, match="Email already exists"):
        use_case.execute(
            creator=manager_alice,
            first_name="Jane",
            last_name="Doe",
            email=existing_email,
            password="securepassword",
            phone_number="0987654321",
            role=Role.MANAGEMENT,
        )

    assert len(collaborator_repository.collaborators) == 1


def test_support_cannot_create_collaborator(bob_support, collaborator_repository, data_john_doe, uuid_generator):
    auth_context = AuthContext(bob_support)
    use_case = CreateCollaboratorUseCase(collaborator_repository, uuid_generator, auth_context)

    with pytest.raises(PermissionError, match="You do not have permission to perform this action"):
        use_case.execute(creator=bob_support, **data_john_doe)

    assert len(collaborator_repository.collaborators) == 0

    auth_context = AuthContext(bob_support)
    use_case = CreateCollaboratorUseCase(collaborator_repository, uuid_generator, auth_context)

    with pytest.raises(PermissionError, match="You do not have permission to perform this action"):
        use_case.execute(creator=bob_support, **data_john_doe)

    assert len(collaborator_repository.collaborators) == 0


def test_commercial_cannot_create_collaborator(
    john_commercial, collaborator_repository, data_john_doe, uuid_generator
):
    auth_context = AuthContext(john_commercial)
    use_case = CreateCollaboratorUseCase(collaborator_repository, uuid_generator, auth_context)

    with pytest.raises(PermissionError, match="You do not have permission to perform this action"):
        use_case.execute(creator=john_commercial, **data_john_doe)

    assert len(collaborator_repository.collaborators) == 0
