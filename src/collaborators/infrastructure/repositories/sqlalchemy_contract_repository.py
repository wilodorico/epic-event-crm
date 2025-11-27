from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from collaborators.domain.contract.contract import Contract, ContractStatus
from collaborators.infrastructure.database.models.contract import ContractModel
from collaborators.infrastructure.mappers.contract import ContractMapper


class SqlalchemyContractRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, contract: Contract) -> None:
        model = ContractMapper.to_model(contract)
        self.session.add(model)
        self.session.commit()

    def find_by_id(self, contract_id: str) -> Contract | None:
        query = select(ContractModel).where(ContractModel.id == contract_id)
        contract_model = self.session.execute(query).scalar_one_or_none()
        if contract_model:
            return ContractMapper.to_entity(contract_model)
        return None

    def find_by_customer_id(self, customer_id: str) -> list[Contract]:
        query = select(ContractModel).where(ContractModel.customer_id == customer_id)
        contract_models = self.session.execute(query).scalars().all()
        if contract_models:
            return [ContractMapper.to_entity(model) for model in contract_models]
        return []

    def update(self, contract: Contract) -> None:
        model = ContractMapper.to_model(contract)
        self.session.merge(model)
        self.session.commit()

    def count(self) -> int:
        """Count all contracts in the database."""
        query = select(func.count(ContractModel.id))
        result = self.session.execute(query)
        return result.scalar()

    def get_all(self) -> list[Contract]:
        """Retrieve all contracts from the database."""
        query = select(ContractModel)
        result = self.session.execute(query)
        contract_models = result.scalars().all()
        return [ContractMapper.to_entity(model) for model in contract_models]

    def get_all_unsigned(self, commercial_id: str) -> list[Contract]:
        """Retrieve all unsigned contracts for a given commercial from the database."""
        query = select(ContractModel).where(
            ContractModel.commercial_id == commercial_id,
            ContractModel.status == ContractStatus.PENDING.value,
        )
        result = self.session.execute(query)
        contract_models = result.scalars().all()
        return [ContractMapper.to_entity(model) for model in contract_models]

    def get_all_unpaid(self, commercial_id: str) -> list[Contract]:
        """Retrieve all unpaid contracts for a given commercial from the database."""
        query = select(ContractModel).where(
            ContractModel.commercial_id == commercial_id,
            ContractModel.remaining_amount > 0,
        )
        result = self.session.execute(query)
        contract_models = result.scalars().all()
        return [ContractMapper.to_entity(model) for model in contract_models]

    def get_all_with_relations(self) -> list[Contract]:
        """Retrieve all contracts with customer and commercial data (optimized)."""
        query = select(ContractModel).options(
            joinedload(ContractModel.customer),
            joinedload(ContractModel.commercial),
            joinedload(ContractModel.created_by),
        )
        result = self.session.execute(query)
        contract_models = result.scalars().unique().all()
        return [ContractMapper.to_entity(model) for model in contract_models]

    def get_all_unsigned_with_relations(self, commercial_id: str) -> list[Contract]:
        """Retrieve unsigned contracts with customer data for performance."""
        query = (
            select(ContractModel)
            .options(joinedload(ContractModel.customer))
            .where(
                ContractModel.commercial_id == commercial_id,
                ContractModel.status == ContractStatus.PENDING.value,
            )
        )
        result = self.session.execute(query)
        contract_models = result.scalars().unique().all()
        return [ContractMapper.to_entity(model) for model in contract_models]

    def get_all_unpaid_with_relations(self, commercial_id: str) -> list[Contract]:
        """Retrieve unpaid contracts with customer data for performance."""
        query = (
            select(ContractModel)
            .options(joinedload(ContractModel.customer))
            .where(
                ContractModel.commercial_id == commercial_id,
                ContractModel.remaining_amount > 0,
            )
        )
        result = self.session.execute(query)
        contract_models = result.scalars().unique().all()
        return [ContractMapper.to_entity(model) for model in contract_models]
