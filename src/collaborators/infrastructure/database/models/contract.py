from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship

from .base import Base


class ContractModel(Base):
    __tablename__ = "contracts"

    id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False, index=True)
    commercial_id = Column(String, ForeignKey("collaborators.id"), nullable=False, index=True)
    created_by_id = Column(String, ForeignKey("collaborators.id"), nullable=False, index=True)
    total_amount = Column(DECIMAL, nullable=False)
    remaining_amount = Column(DECIMAL, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by_id = Column(String, ForeignKey("collaborators.id"), nullable=True, index=True)

    # Relations
    customer = relationship("CustomerModel", back_populates="contracts")
    commercial = relationship("CollaboratorModel", foreign_keys=[commercial_id], back_populates="contracts")
    created_by = relationship("CollaboratorModel", foreign_keys=[created_by_id], back_populates="created_contracts")
    updated_by = relationship("CollaboratorModel", foreign_keys=[updated_by_id])
    events = relationship("EventModel", back_populates="contract")
