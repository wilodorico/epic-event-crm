import pytest

from adapters.fixed_id_generator import FixedIdGenerator
from adapters.in_memory_collaborator_repository import InMemoryCollaboratorRepository
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
def john_doe():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "password": "securepassword",
        "phone_number": "1234567890",
        "role": "Management",
    }


def test_create_collaborator_use_case_success(use_case, repository, john_doe):
    use_case.execute(**john_doe)

    collaborator = repository.find_by_email("john.doe@test.com")

    assert len(repository.collaborators) == 1
    assert collaborator.id == "id-1"
    assert collaborator.first_name == "John"
    assert collaborator.last_name == "Doe"
    assert collaborator.email == "john.doe@test.com"
    assert collaborator.phone_number == "1234567890"
    assert collaborator.role == "Management"


def test_cannot_create_collaborator_with_existing_email(use_case, repository, john_doe):
    use_case.execute(**john_doe)

    with pytest.raises(ValueError, match="Email already exists"):
        use_case.execute(
            first_name="Jane",
            last_name="Doe",
            email="john.doe@test.com",
            password="securepassword",
            phone_number="0987654321",
            role="Management",
        )

    assert len(repository.collaborators) == 1
