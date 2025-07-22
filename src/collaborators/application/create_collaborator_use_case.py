from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.domain.collaborator.collaborator_repository_abc import CollaboratorRepositoryABC
from commons.id_generator_abc import IdGeneratorABC


class CreateCollaboratorUseCase:
    def __init__(
        self, repository: CollaboratorRepositoryABC, id_generator: IdGeneratorABC, auth_context: AuthContextABC
    ):
        self._repository = repository
        self._id_generator = id_generator
        self._auth_context = auth_context

    def execute(
        self,
        creator: Collaborator,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        phone_number: str,
        role: str,
    ) -> None:
        self._auth_context.ensure_can_create_collaborator()

        if self._repository.find_by_email(email):
            raise ValueError("Email already exists")

        id = self._id_generator.generate()

        collaborator = Collaborator(
            id=id,
            created_by_id=creator.id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone_number=phone_number,
            role=role,
        )
        self._repository.create(collaborator)
        self._repository.create(collaborator)
