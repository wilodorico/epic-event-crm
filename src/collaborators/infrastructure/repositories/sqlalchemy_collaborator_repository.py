from sqlalchemy.orm import Session

from collaborators.domain.collaborator.collaborator import Collaborator
from collaborators.infrastructure.database.models.collaborator import CollaboratorModel
from collaborators.infrastructure.mappers.collaborator import CollaboratorMapper


class SqlalchemyCollaboratorRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, collaborator: Collaborator) -> None:
        model = CollaboratorMapper.to_model(collaborator)
        self.session.add(model)
        self.session.commit()

    def find_by_email(self, email: str) -> Collaborator | None:
        collaborator_model = self.session.query(CollaboratorModel).filter_by(email=email).first()
        if collaborator_model:
            return CollaboratorMapper.to_entity(collaborator_model)
        return None

    def find_by_id(self, collaborator_id: str) -> Collaborator | None:
        raise NotImplementedError()

    def update(self, collaborator: Collaborator) -> None:
        raise NotImplementedError()

    def delete(self, collaborator_id: str) -> None:
        raise NotImplementedError()
