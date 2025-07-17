from entities.collaborator import Collaborator


class InMemoryCollaboratorRepository:
    def __init__(self):
        self.collaborators: dict[str, Collaborator] = {}

    def create(self, collaborator: Collaborator) -> None:
        self.collaborators[collaborator.id] = collaborator

    def find_by_email(self, email: str) -> Collaborator | None:
        return next((c for c in self.collaborators.values() if c.email == email), None)
