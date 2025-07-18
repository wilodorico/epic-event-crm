import pytest

from adapters.fixed_id_generator import FixedIdGenerator
from adapters.in_memory_collaborator_repository import InMemoryCollaboratorRepository
from entities.collaborator import Collaborator, Role
from usecases.create_collaborator import CreateCollaboratorUseCase


@pytest.fixture
def repository():
    return InMemoryCollaboratorRepository()


@pytest.fixture
def fixed_id_generator():
    return FixedIdGenerator()


@pytest.fixture
def use_case(repository, fixed_id_generator):
    return CreateCollaboratorUseCase(repository, fixed_id_generator)


@pytest.fixture
def manager_creator():
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
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "password": "securepassword",
        "phone_number": "1234567890",
        "role": Role.MARKETING,
    }


def test_create_collaborator_use_case_success(use_case, repository, john_doe, manager_creator):
    use_case.execute(creator=manager_creator, **john_doe)

    collaborator = repository.find_by_email("john.doe@test.com")

    assert len(repository.collaborators) == 1
    assert collaborator.id == "id-1"
    assert collaborator.first_name == "John"
    assert collaborator.last_name == "Doe"
    assert collaborator.email == "john.doe@test.com"
    assert collaborator.phone_number == "1234567890"
    assert collaborator.role == Role.MARKETING


def test_cannot_create_collaborator_with_existing_email(use_case, repository, john_doe, manager_creator):
    use_case.execute(creator=manager_creator, **john_doe)
    existing_email = john_doe["email"]

    with pytest.raises(ValueError, match="Email already exists"):
        use_case.execute(
            creator=manager_creator,
            first_name="Jane",
            last_name="Doe",
            email=existing_email,
            password="securepassword",
            phone_number="0987654321",
            role="Management",
        )

    assert len(repository.collaborators) == 1


def test_non_manager_cannot_create_collaborator(use_case, repository, john_doe):
    non_manager = Collaborator(
        id="creator-1",
        created_by_id="1",
        first_name="Bob",
        last_name="Support",
        email="support@test.com",
        password="pass",
        phone_number="123456789",
        role=Role.SUPPORT,
    )
    with pytest.raises(PermissionError, match="Only managers can create collaborators"):
        use_case.execute(creator=non_manager, **john_doe)

    assert len(repository.collaborators) == 0
