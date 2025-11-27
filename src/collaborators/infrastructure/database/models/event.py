from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from .base import Base


class EventModel(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    contract_id = Column(String(36), ForeignKey("contracts.id"), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(255), nullable=False)
    attendee = Column(Integer, nullable=False)
    notes = Column(String(1000), nullable=True)
    contact_support_id = Column(String(36), ForeignKey("collaborators.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    updated_by_id = Column(String(36), ForeignKey("collaborators.id"), nullable=True)

    # Relations
    customer = relationship("CustomerModel", back_populates="events")
    contract = relationship("ContractModel", back_populates="events")
    support_contact = relationship(
        "CollaboratorModel", foreign_keys=[contact_support_id], back_populates="assigned_events"
    )
    updated_by = relationship("CollaboratorModel", foreign_keys=[updated_by_id])
