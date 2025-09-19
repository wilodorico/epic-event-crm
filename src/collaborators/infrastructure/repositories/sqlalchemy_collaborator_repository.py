from sqlalchemy import select
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
        stmt = select(CollaboratorModel).where(CollaboratorModel.email == email)
        collaborator_model = self.session.execute(stmt).scalar_one_or_none()
        if collaborator_model:
            return CollaboratorMapper.to_entity(collaborator_model)
        return None

    def find_by_id(self, collaborator_id: str) -> Collaborator | None:
        stmt = select(CollaboratorModel).where(CollaboratorModel.id == collaborator_id)
        collaborator_model = self.session.execute(stmt).scalar_one_or_none()
        if collaborator_model:
            return CollaboratorMapper.to_entity(collaborator_model)
        return None

    def count(self) -> int:
        """Count all collaborators in the database."""
        stmt = select(CollaboratorModel)
        result = self.session.execute(stmt)
        return len(result.scalars().all())

    def update(self, collaborator: Collaborator) -> None:
        """Update an existing collaborator."""
        model = CollaboratorMapper.to_model(collaborator)
        # Merge updates the existing record with the same primary key
        self.session.merge(model)
        self.session.commit()

    def delete(self, collaborator_id: str) -> None:
        """Delete a collaborator by ID."""
        stmt = select(CollaboratorModel).where(CollaboratorModel.id == collaborator_id)
        collaborator_model = self.session.execute(stmt).scalar_one_or_none()
        if collaborator_model:
            self.session.delete(collaborator_model)
            self.session.commit()
