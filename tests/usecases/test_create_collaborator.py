from adapters.fixed_id_generator import FixedIdGenerator
from adapters.in_memory_collaborator_repository import InMemoryCollaboratorRepository
from usecases.create_collaborator import CreateCollaboratorUseCase


def test_create_collaborator_use_case_success():
    id_generator = FixedIdGenerator()
    repository = InMemoryCollaboratorRepository()
    use_case = CreateCollaboratorUseCase(repository, id_generator)

    use_case.execute(
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        password="securepassword",
        phone_number="1234567890",
        role="Management",
    )

    collaborator = repository.find_by_email("john.doe@test.com")

    assert len(repository.collaborators) == 1
    assert collaborator.id == "id-1"
    assert collaborator.first_name == "John"
    assert collaborator.last_name == "Doe"
    assert collaborator.email == "john.doe@test.com"
    assert collaborator.phone_number == "1234567890"
    assert collaborator.role == "Management"
