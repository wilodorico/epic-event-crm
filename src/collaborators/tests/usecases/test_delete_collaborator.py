from collaborators.application.delete_collaborator_use_case import DeleteCollaboratorUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.infrastructure.in_memory_collaborator_repository import InMemoryCollaboratorRepository


def test_manager_can_delete_collaborator_success(manager_alice, fixed_id_generator, john_doe):
    auth_context = AuthContext(manager_alice)
    repository = InMemoryCollaboratorRepository()
    repository.create(john_doe)
    use_case = DeleteCollaboratorUseCase(repository, fixed_id_generator, auth_context)
    collaborator_to_delete = repository.find_by_id("john-id-1")
    use_case.execute(manager_alice, collaborator_to_delete.id)
    assert repository.find_by_id("john-id-1") is None
