from sqlalchemy import Column, DateTime, String, func

from .base import Base


class CollaboratorModel(Base):
    __tablename__ = "collaborators"

    id = Column(String, primary_key=True, index=True)
    created_by_id = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    updated_by_id = Column(String, nullable=True)
