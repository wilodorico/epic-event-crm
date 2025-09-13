from sqlalchemy import Column, DateTime, Enum, String, func

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
    role = Column(Enum(Role, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    updated_by_id = Column(String, nullable=True)
