from collaborators.domain.collaborator.collaborator import Collaborator


class InMemoryCollaboratorRepository:
    def __init__(self):
        self.collaborators: dict[str, Collaborator] = {}

    def create(self, collaborator: Collaborator) -> None:
        self.collaborators[collaborator.id] = collaborator

    def find_by_email(self, email: str) -> Collaborator | None:
        return next((c for c in self.collaborators.values() if c.email == email), None)

    def find_by_id(self, collaborator_id: str) -> Collaborator | None:
        return self.collaborators.get(collaborator_id)

    def update(self, collaborator: Collaborator) -> None:
        self.collaborators[collaborator.id] = collaborator

    def delete(self, collaborator_id: str) -> None:
        del self.collaborators[collaborator_id]
