import pytest

from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.in_memory_collaborator_repository import InMemoryCollaboratorRepository
from commons.fixed_id_generator import FixedIdGenerator


@pytest.fixture
def repository():
    return InMemoryCollaboratorRepository()


@pytest.fixture
def fixed_id_generator():
    return FixedIdGenerator()


@pytest.fixture
def manager_alice():
    return Collaborator(
        id="creator-id",
        created_by_id="1",
        first_name="Alice",
        last_name="Smith",
        email="alice.smith@test.com",
        password="securepassword",
        phone_number="1112223333",
        role=Role.MANAGEMENT,
    )


@pytest.fixture
def john_doe():
    return Collaborator(
        id="john-id-1",
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        password="securepassword",
        phone_number="1234567890",
        role=Role.MARKETING,
        created_by_id="creator-id",
    )
