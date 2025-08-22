import pytest

from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.in_memory_collaborator_repository import InMemoryCollaboratorRepository
from commons.fixed_id_generator import FixedIdGenerator


@pytest.fixture
def collaborator_repository():
    return InMemoryCollaboratorRepository()


@pytest.fixture
def fixed_id_generator():
    return FixedIdGenerator()


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
