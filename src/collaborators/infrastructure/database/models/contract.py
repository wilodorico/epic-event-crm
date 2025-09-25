from sqlalchemy import DECIMAL, Column, DateTime, String, func

from .base import Base


class ContractModel(Base):
    __tablename__ = "contracts"

    id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False, index=True)
    commercial_id = Column(String, nullable=False, index=True)
    created_by_id = Column(String, nullable=False, index=True)
    total_amount = Column(DECIMAL, nullable=False)
    remaining_amount = Column(DECIMAL, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by_id = Column(String, nullable=True, index=True)
