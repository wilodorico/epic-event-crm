from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, String

from collaborators.domain.collaborator.collaborator import Role

from ..db import Base


class CollaboratorModel(Base):
    __tablename__ = "collaborators"

    id = Column(String, primary_key=True, index=True)
    created_by_id = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)
    created_at = Column(DateTime, default=datetime.timezone.utc)
    updated_at = Column(DateTime, default=datetime.timezone.utc, onupdate=datetime.timezone.utc)
