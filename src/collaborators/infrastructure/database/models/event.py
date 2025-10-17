from sqlalchemy import Column, DateTime, Integer, String, func

from .base import Base


class EventModel(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    customer_id = Column(String, nullable=False)
    contract_id = Column(String, nullable=False)
    date_start = Column(DateTime(timezone=True), nullable=False)
    date_end = Column(DateTime(timezone=True), nullable=False)
    location = Column(String, nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    contact_support_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    updated_by_id = Column(String, nullable=True)
