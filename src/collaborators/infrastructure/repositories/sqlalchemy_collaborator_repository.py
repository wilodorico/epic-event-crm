from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

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
        query = select(CollaboratorModel).where(CollaboratorModel.email == email)
        collaborator_model = self.session.execute(query).scalar_one_or_none()
        if collaborator_model:
            return CollaboratorMapper.to_entity(collaborator_model)
        return None

    def find_by_id(self, collaborator_id: str) -> Collaborator | None:
        query = select(CollaboratorModel).where(CollaboratorModel.id == collaborator_id)
        collaborator_model = self.session.execute(query).scalar_one_or_none()
        if collaborator_model:
            return CollaboratorMapper.to_entity(collaborator_model)
        return None

    def count(self) -> int:
        """Count all collaborators in the database."""
        query = select(func.count(CollaboratorModel.id))
        result = self.session.execute(query)
        return result.scalar()

    def update(self, collaborator: Collaborator) -> None:
        """Update an existing collaborator."""
        model = CollaboratorMapper.to_model(collaborator)
        # Merge updates the existing record with the same primary key
        self.session.merge(model)
        self.session.commit()

    def delete(self, collaborator_id: str) -> None:
        """Delete a collaborator by ID."""
        query = select(CollaboratorModel).where(CollaboratorModel.id == collaborator_id)
        collaborator_model = self.session.execute(query).scalar_one_or_none()
        if collaborator_model:
            self.session.delete(collaborator_model)
            self.session.commit()

    def find_by_id_with_relations(self, collaborator_id: str) -> Collaborator | None:
        """Find collaborator by ID with created_by and updated_by data (optimized)."""
        query = (
            select(CollaboratorModel)
            .options(joinedload(CollaboratorModel.created_by), joinedload(CollaboratorModel.updated_by))
            .where(CollaboratorModel.id == collaborator_id)
        )
        collaborator_model = self.session.execute(query).scalar_one_or_none()
        if collaborator_model:
            return CollaboratorMapper.to_entity(collaborator_model)
        return None

    def get_commercials_with_customers(self) -> list[Collaborator]:
        """Get all commercial collaborators with their customers (optimized)."""
        query = (
            select(CollaboratorModel)
            .options(selectinload(CollaboratorModel.customers))
            .where(CollaboratorModel.role == "Commercial")
        )
        result = self.session.execute(query)
        collaborator_models = result.scalars().unique().all()
        return [CollaboratorMapper.to_entity(model) for model in collaborator_models]

    def get_managers_with_created_entities(self) -> list[Collaborator]:
        """Get management collaborators with entities they created (optimized)."""
        query = (
            select(CollaboratorModel)
            .options(selectinload(CollaboratorModel.created_contracts))
            .where(CollaboratorModel.role == "Management")
        )
        result = self.session.execute(query)
        collaborator_models = result.scalars().unique().all()
        return [CollaboratorMapper.to_entity(model) for model in collaborator_models]
