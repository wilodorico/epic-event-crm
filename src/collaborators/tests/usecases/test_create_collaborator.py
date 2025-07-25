import pytest

from collaborators.application.create_collaborator_use_case import CreateCollaboratorUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.collaborator import Collaborator, Role


@pytest.fixture
def data_john_doe():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "password": "securepassword",
        "phone_number": "1234567890",
        "role": Role.MARKETING,
    }


def test_manager_can_create_collaborator(repository, data_john_doe, manager_alice, fixed_id_generator):
    auth_context = AuthContext(manager_alice)
    use_case = CreateCollaboratorUseCase(repository, fixed_id_generator, auth_context)
    use_case.execute(creator=manager_alice, **data_john_doe)

    collaborator = repository.find_by_email("john.doe@test.com")

    assert len(repository.collaborators) == 1
    assert collaborator.id == "id-1"
    assert collaborator.first_name == "John"
    assert collaborator.last_name == "Doe"
    assert collaborator.email == "john.doe@test.com"
    assert collaborator.phone_number == "1234567890"
    assert collaborator.role == Role.MARKETING


def test_manager_cannot_create_collaborator_with_existing_email(
    repository, data_john_doe, manager_alice, fixed_id_generator
):
    auth_context = AuthContext(manager_alice)
    use_case = CreateCollaboratorUseCase(repository, fixed_id_generator, auth_context)
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
            role="Management",
        )

    assert len(repository.collaborators) == 1


def test_support_cannot_create_collaborator(repository, data_john_doe, fixed_id_generator):
    support_user = Collaborator(
        id="support-1",
        created_by_id="1",
        first_name="Bob",
        last_name="Support",
        email="support@test.com",
        password="pass",
        phone_number="123456789",
        role=Role.SUPPORT,
    )

    auth_context = AuthContext(support_user)
    use_case = CreateCollaboratorUseCase(repository, fixed_id_generator, auth_context)

    with pytest.raises(PermissionError, match="You do not have permission to perform this action"):
        use_case.execute(creator=support_user, **data_john_doe)

    assert len(repository.collaborators) == 0


def test_marketing_cannot_create_collaborator(repository, data_john_doe, fixed_id_generator):
    marketing_user = Collaborator(
        id="marketing-1",
        created_by_id="1",
        first_name="Carol",
        last_name="Marketing",
        email="marketing@test.com",
        password="pass",
        phone_number="123456789",
        role=Role.MARKETING,
    )

    auth_context = AuthContext(marketing_user)
    use_case = CreateCollaboratorUseCase(repository, fixed_id_generator, auth_context)

    with pytest.raises(PermissionError, match="You do not have permission to perform this action"):
        use_case.execute(creator=marketing_user, **data_john_doe)

    assert len(repository.collaborators) == 0
