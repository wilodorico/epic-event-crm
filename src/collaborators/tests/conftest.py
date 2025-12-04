import os
from contextlib import closing
from datetime import datetime, timedelta

import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.domain.contract.contract import Contract
from collaborators.domain.customer.customer import Customer
from collaborators.domain.event.event import Event
from collaborators.infrastructure.database.models.base import Base
from collaborators.infrastructure.repositories.in_memory_collaborator_repository import InMemoryCollaboratorRepository
from collaborators.infrastructure.repositories.in_memory_contract_repository import InMemoryContractRepository
from collaborators.infrastructure.repositories.in_memory_customer_repository import InMemoryCustomerRepository
from collaborators.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository
from collaborators.infrastructure.repositories.sqlalchemy_customer_repository import SqlalchemyCustomerRepository
from collaborators.infrastructure.repositories.sqlalchemy_event_repository import SqlalchemyEventRepository
from collaborators.tests.fakes.fake_password_hasher import FakePasswordHasher
from commons.uuid_generator import UuidGenerator


@pytest.fixture
def session():
    """Session SQLite in-memory for tests."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    Base.metadata.create_all(bind=engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with closing(TestSessionLocal()) as session:
        yield session


@pytest.fixture
def collaborator_repository(session):
    """Repository fixture switching between in-memory and SQLAlchemy based on env var USE_SQLALCHEMY_REPO."""
    if os.getenv("USE_SQLALCHEMY_REPO") == "1":
        return SqlalchemyCollaboratorRepository(session)
    return InMemoryCollaboratorRepository()


@pytest.fixture
def customer_repository(session):
    """Repository fixture switching between in-memory and SQLAlchemy based on env var USE_SQLALCHEMY_REPO."""
    if os.getenv("USE_SQLALCHEMY_REPO") == "1":
        return SqlalchemyCustomerRepository(session)
    return InMemoryCustomerRepository()


@pytest.fixture
def contract_repository(session):
    """Repository fixture switching between in-memory and SQLAlchemy based on env var USE_SQLALCHEMY_REPO."""
    if os.getenv("USE_SQLALCHEMY_REPO") == "1":
        return SqlalchemyContractRepository(session)
    return InMemoryContractRepository()


@pytest.fixture
def event_repository(session):
    """Repository fixture switching between in-memory and SQLAlchemy based on env var USE_SQLALCHEMY_REPO."""
    if os.getenv("USE_SQLALCHEMY_REPO") == "1":
        return SqlalchemyEventRepository(session)
    return InMemoryEventRepository()


@pytest.fixture
def uuid_generator():
    return UuidGenerator()


@pytest.fixture
def password_hasher():
    return FakePasswordHasher()


@pytest.fixture
def manager_alice():
    return Collaborator(
        id="creator-id",
        created_by_id="admin-id-1",
        first_name="Alice",
        last_name="Smith",
        email="alice.smith@test.com",
        password="securepassword",
        phone_number="1112223333",
        role=Role.MANAGEMENT,
    )


@pytest.fixture
def john_commercial():
    return Collaborator(
        id="john-commercial-1",
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        password="securepassword",
        phone_number="1234567890",
        role=Role.COMMERCIAL,
        created_by_id="creator-id",
    )


@pytest.fixture
def amel_commercial():
    return Collaborator(
        id="amel-commercial-1",
        first_name="Amel",
        last_name="Doe",
        email="amel.doe@test.com",
        password="securepassword",
        phone_number="1234567890",
        role=Role.COMMERCIAL,
        created_by_id="creator-id",
    )


@pytest.fixture
def jane_commercial():
    return Collaborator(
        id="jane-commercial-1",
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@test.com",
        password="securepassword",
        phone_number="1234567890",
        role=Role.COMMERCIAL,
        created_by_id="creator-id",
    )


@pytest.fixture
def bob_support():
    return Collaborator(
        id="bob-support-1",
        first_name="Bob",
        last_name="Builder",
        email="bob.builder@test.com",
        password="securepassword",
        phone_number="9876543210",
        role=Role.SUPPORT,
        created_by_id="creator-id",
    )


@pytest.fixture
def florence_support():
    return Collaborator(
        id="florence-support-1",
        first_name="Florence",
        last_name="bonumeur",
        email="florence.bonumeur@test.com",
        password="securepassword",
        phone_number="1234567890",
        role=Role.SUPPORT,
        created_by_id="creator-id",
    )


@pytest.fixture
def carol_marketing():
    return Collaborator(
        id="carol-marketing-1",
        created_by_id="1",
        first_name="Carol",
        last_name="Marketing",
        email="marketing@test.com",
        password="pass",
        phone_number="123456789",
        role=Role.COMMERCIAL,
    )


@pytest.fixture
def karim_customer(john_commercial):
    return Customer(
        id="karim-customer-1",
        first_name="Karim",
        last_name="Denour",
        email="karim.denour@test.com",
        phone_number="1234567890",
        company="Ks Corp",
        commercial_contact_id=john_commercial.id,
    )


@pytest.fixture
def marie_customer(amel_commercial):
    return Customer(
        id="marie-customer-1",
        first_name="Marie",
        last_name="Legrand",
        email="marie.legrand@test.com",
        phone_number="1234567890",
        company="Test Corp",
        commercial_contact_id=amel_commercial.id,
    )


@pytest.fixture
def karim_contract(manager_alice, karim_customer, john_commercial):
    return Contract(
        id="karim-contract-1",
        customer_id=karim_customer.id,
        commercial_id=john_commercial.id,
        created_by_id=manager_alice.id,
        total_amount=1000.00,
        remaining_amount=1000.00,
    )


@pytest.fixture
def karim_paid_contract(manager_alice, karim_customer, john_commercial):
    return Contract(
        id="karim-contract-2",
        customer_id=karim_customer.id,
        commercial_id=john_commercial.id,
        created_by_id=manager_alice.id,
        total_amount=1500.00,
        remaining_amount=0.00,
    )


@pytest.fixture
def marie_contract(manager_alice, marie_customer, amel_commercial):
    return Contract(
        id="marie-contract-1",
        customer_id=marie_customer.id,
        commercial_id=amel_commercial.id,
        created_by_id=manager_alice.id,
        total_amount=2000.00,
        remaining_amount=2000.00,
    )


@pytest.fixture
def karim_event(karim_contract):
    return Event(
        id="karim-event-1",
        customer_id=karim_contract.customer_id,
        contract_id=karim_contract.id,
        title="Karim's Event",
        date_start=datetime.now() + timedelta(days=30),
        date_end=datetime.now() + timedelta(days=30, hours=8),
        location="Karim's Venue",
        attendees=50,
        notes="Initial event setup",
    )


@pytest.fixture
def karim_past_event(karim_contract):
    return Event(
        id="karim-past-event-1",
        customer_id=karim_contract.customer_id,
        contract_id=karim_contract.id,
        title="Karim's Past Event",
        date_start=datetime(2024, 5, 1, 10, 0),
        date_end=datetime(2024, 5, 1, 18, 0),
        location="Karim's Old Venue",
        attendees=50,
        notes="Past event setup",
    )


@pytest.fixture
def marie_event(marie_contract):
    return Event(
        id="marie-event-1",
        customer_id=marie_contract.customer_id,
        contract_id=marie_contract.id,
        title="Marie's Event",
        date_start=datetime.now() + timedelta(days=30),
        date_end=datetime.now() + timedelta(days=30, hours=8),
        location="Marie's Venue",
        attendees=100,
        notes="Initial event setup for Marie",
    )
