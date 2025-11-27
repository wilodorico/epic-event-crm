from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship

from .base import Base


class CollaboratorModel(Base):
    __tablename__ = "collaborators"

    id = Column(String, primary_key=True, index=True)
    created_by_id = Column(String, ForeignKey("collaborators.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    updated_by_id = Column(String, ForeignKey("collaborators.id"), nullable=True)

    # Relations
    created_by = relationship("CollaboratorModel", remote_side=[id], foreign_keys=[created_by_id], post_update=True)
    updated_by = relationship("CollaboratorModel", remote_side=[id], foreign_keys=[updated_by_id], post_update=True)
    customers = relationship(
        "CustomerModel", foreign_keys="CustomerModel.commercial_contact_id", back_populates="commercial_contact"
    )
    contracts = relationship("ContractModel", foreign_keys="ContractModel.commercial_id", back_populates="commercial")
    created_contracts = relationship(
        "ContractModel", foreign_keys="ContractModel.created_by_id", back_populates="created_by"
    )
    assigned_events = relationship(
        "EventModel", foreign_keys="EventModel.contact_support_id", back_populates="support_contact"
    )
