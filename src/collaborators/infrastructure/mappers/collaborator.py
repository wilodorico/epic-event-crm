from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.database.models.collaborator import CollaboratorModel


class CollaboratorMapper:
    @staticmethod
    def to_entity(model: CollaboratorModel) -> Collaborator:
        return Collaborator(
            id=model.id,
            created_by_id=model.created_by_id,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            password=model.password,
            phone_number=model.phone_number,
            role=Role(model.role),
            created_at=model.created_at,
            updated_at=model.updated_at,
            updated_by_id=model.updated_by_id,
        )

    @staticmethod
    def to_model(entity: Collaborator) -> CollaboratorModel:
        return CollaboratorModel(
            id=entity.id,
            created_by_id=entity.created_by_id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            password=entity.password,
            phone_number=entity.phone_number,
            role=entity.role.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            updated_by_id=entity.updated_by_id,
        )
