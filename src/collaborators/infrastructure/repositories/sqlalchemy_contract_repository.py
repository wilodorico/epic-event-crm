from sqlalchemy import select
from sqlalchemy.orm import Session

from collaborators.domain.contract.contract import Contract
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
        stmt = select(ContractModel).where(ContractModel.id == contract_id)
        contract_model = self.session.execute(stmt).scalar_one_or_none()
        if contract_model:
            return ContractMapper.to_entity(contract_model)
        return None

    def find_by_customer_id(self, customer_id: str) -> list[Contract] | list:
        stmt = select(ContractModel).where(ContractModel.customer_id == customer_id)
        contract_models = self.session.execute(stmt).scalars().all()
        if contract_models:
            return [ContractMapper.to_entity(model) for model in contract_models]
        return []

    def update(self, contract: Contract) -> None:
        model = ContractMapper.to_model(contract)
        self.session.merge(model)
        self.session.commit()

    def get_all(self) -> list[Contract] | list:
        """Retrieve all contracts from the database."""
        stmt = select(ContractModel)
        result = self.session.execute(stmt)
        contract_models = result.scalars().all()
        return [ContractMapper.to_entity(model) for model in contract_models]
