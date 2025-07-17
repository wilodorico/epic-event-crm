from entities.collaborator import Collaborator
from ports.collaborator_repository_abc import CollaboratorRepositoryABC
from ports.id_generator_abc import IdGeneratorABC


class CreateCollaboratorUseCase:
    def __init__(self, repository: CollaboratorRepositoryABC, id_generator: IdGeneratorABC):
        self._repository = repository
        self._id_generator = id_generator

    def execute(
        self, first_name: str, last_name: str, email: str, password: str, phone_number: str, role: str
    ) -> None:
        if self._repository.find_by_email(email):
            raise ValueError("Email already exists")

        id = self._id_generator.generate()

        collaborator = Collaborator(
            id=id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone_number=phone_number,
            role=role,
        )
        self._repository.create(collaborator)
