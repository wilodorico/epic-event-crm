from collaborators.domain.contract.contract import Contract, ContractStatus
from collaborators.infrastructure.database.models.contract import ContractModel


class ContractMapper:
    @staticmethod
    def to_entity(model: ContractModel) -> Contract:
        contract = Contract(
            id=model.id,
            customer_id=model.customer_id,
            commercial_id=model.commercial_id,
            created_by_id=model.created_by_id,
            total_amount=model.total_amount,
            remaining_amount=model.remaining_amount,
        )
        # Override the auto-generated values with DB values
        contract.created_at = model.created_at
        contract.updated_at = model.updated_at
        contract.updated_by_id = model.updated_by_id
        contract.status = ContractStatus(model.status)
        return contract

    @staticmethod
    def to_model(entity: Contract) -> ContractModel:
        model = ContractModel(
            id=entity.id,
            customer_id=entity.customer_id,
            commercial_id=entity.commercial_id,
            created_by_id=entity.created_by_id,
            total_amount=float(entity.total_amount),
            remaining_amount=float(entity.remaining_amount),
            status=entity.status.value,
            updated_by_id=entity.updated_by_id,
        )
        # Set timestamps manually if they exist
        if entity.created_at:
            model.created_at = entity.created_at
        if entity.updated_at:
            model.updated_at = entity.updated_at
        return model
