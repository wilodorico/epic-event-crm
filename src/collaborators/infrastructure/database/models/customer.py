from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship

from .base import Base


class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone_number = Column(String, nullable=False)
    company = Column(String, nullable=False)
    commercial_contact_id = Column(String, ForeignKey("collaborators.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relations
    commercial_contact = relationship(
        "CollaboratorModel", foreign_keys=[commercial_contact_id], back_populates="customers"
    )
    contracts = relationship("ContractModel", back_populates="customer")
    events = relationship("EventModel", back_populates="customer")
