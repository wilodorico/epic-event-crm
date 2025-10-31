from collaborators.application.services.auth_context_abc import AuthContextABC
from collaborators.application.services.password_hasher_abc import PasswordHasherABC
from collaborators.application.use_case_abc import UseCaseABC
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.domain.collaborator.collaborator_repository_abc import CollaboratorRepositoryABC
from collaborators.domain.collaborator.permissions import Permissions
from commons.id_generator_abc import IdGeneratorABC


class CreateCollaboratorUseCase(UseCaseABC):
    """Handles the creation of a new collaborator by a manager.

    This use case ensures that only authorized managers can create new collaborators.
    It validates email uniqueness, hashes the password securely, and persists the new
    collaborator record in the repository.
    """

    permissions = Permissions.CREATE_COLLABORATOR

    def __init__(
        self,
        auth_context: AuthContextABC,
        repository: CollaboratorRepositoryABC,
        id_generator: IdGeneratorABC,
        password_hasher: PasswordHasherABC,
    ):
        super().__init__(auth_context)
        self._repository = repository
        self._id_generator = id_generator
        self._password_hasher = password_hasher

    def _execute(
        self,
        creator: Collaborator,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        phone_number: str,
        role: str,
    ) -> None:
        """Creates a new collaborator.

        Args:
            creator: The collaborator performing the creation (usually a manager).
            first_name: First name of the new collaborator.
            last_name: Last name of the new collaborator.
            email: Unique email address for the collaborator.
            password: Plain text password (will be hashed before persistence).
            phone_number: Collaborator’s phone number.
            role: Role of the collaborator (e.g., commercial, support, management).

        Raises:
            ValueError: If the email already exists.
            PermissionError: If the creator lacks permissions.

        Returns:
            None. The collaborator is persisted in the repository.
        """
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
