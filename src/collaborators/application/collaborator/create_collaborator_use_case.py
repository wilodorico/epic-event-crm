from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.services.password_hasher_abc import PasswordHasherABC
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.domain.collaborator.collaborator_repository_abc import CollaboratorRepositoryABC
from collaborators.domain.collaborator.permissions import Permissions
from commons.id_generator_abc import IdGeneratorABC


class CreateCollaboratorUseCase:
    def __init__(
        self,
        repository: CollaboratorRepositoryABC,
        id_generator: IdGeneratorABC,
        auth_context: AuthContextABC,
        password_hasher: PasswordHasherABC,
    ):
        self._repository = repository
        self._id_generator = id_generator
        self._auth_context = auth_context
        self._password_hasher = password_hasher

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
        self._auth_context.ensure(Permissions.CREATE_COLLABORATOR)

        if self._repository.find_by_email(email):
            raise ValueError("Email already exists")

        id = self._id_generator.generate()
        hashed_password = self._password_hasher.hash(password)
        role_enum = Role(role)

        collaborator = Collaborator(
            id=id,
            created_by_id=creator.id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            phone_number=phone_number,
            role=role_enum,
        )
        self._repository.create(collaborator)
