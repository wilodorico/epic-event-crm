from datetime import datetime, timedelta

import pytest

from collaborators.application.event.create_event_use_case import CreateEventUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.domain.contract.contract import ContractStatus


@pytest.fixture
def event_date_start():
    """Common event start date for all tests."""
    return datetime(2025, 12, 15, 9, 0, 0)


@pytest.fixture
def event_date_end():
    """Common event end date for all tests."""
    return datetime(2025, 12, 15, 17, 0, 0)


@pytest.fixture
def event_attendees():
    """Common number of attendees for all tests."""
    return 150


@pytest.fixture
def base_event_data(event_date_start, event_date_end, event_attendees):
    """Base event data dictionary used across tests."""
    return {
        "title": "Annual Meeting",
        "date_start": event_date_start,
        "date_end": event_date_end,
        "location": "Main Conference Hall",
        "attendees": event_attendees,
        "notes": "Bring your ID for entry",
    }


def test_commercial_can_create_event(
    event_repository,
    contract_repository,
    john_commercial,
    uuid_generator,
    karim_contract,
    base_event_data,
    event_date_start,
    event_date_end,
    event_attendees,
):
    karim_contract.sign_contract(updater_id=john_commercial.id)
    contract_repository.create(karim_contract)

    event_data = {**base_event_data, "contract_id": karim_contract.id}

    auth_context = AuthContext(john_commercial)
    use_case = CreateEventUseCase(event_repository, contract_repository, uuid_generator, auth_context)
    created_event = use_case.execute(creator=john_commercial, **event_data)

    assert karim_contract.status == ContractStatus.SIGNED
    assert created_event.id is not None
    assert created_event.title == "Annual Meeting"
    assert created_event.customer_id == karim_contract.customer_id
    assert created_event.contract_id == karim_contract.id
    assert created_event.date_start == event_date_start
    assert created_event.date_end == event_date_end
    assert created_event.location == "Main Conference Hall"
    assert created_event.attendees == event_attendees
    assert created_event.notes == "Bring your ID for entry"


def test_commercial_cannot_create_event_if_contract_not_signed(
    event_repository,
    contract_repository,
    john_commercial,
    uuid_generator,
    karim_contract,
    base_event_data,
):
    contract_repository.create(karim_contract)

    event_data = {**base_event_data, "contract_id": karim_contract.id}

    auth_context = AuthContext(john_commercial)
    use_case = CreateEventUseCase(event_repository, contract_repository, uuid_generator, auth_context)

    with pytest.raises(ValueError, match="Contract must be signed to create an event"):
        use_case.execute(creator=john_commercial, **event_data)


def test_commercial_cannot_create_event_with_non_existent_contract(
    event_repository,
    contract_repository,
    john_commercial,
    uuid_generator,
    base_event_data,
):
    event_data = {**base_event_data, "contract_id": "non-existent-contract-id"}

    auth_context = AuthContext(john_commercial)
    use_case = CreateEventUseCase(event_repository, contract_repository, uuid_generator, auth_context)

    with pytest.raises(ValueError, match="Contract not found"):
        use_case.execute(creator=john_commercial, **event_data)


def test_commercial_cannot_create_event_for_other_commercials_contract(
    event_repository,
    contract_repository,
    john_commercial,
    uuid_generator,
    marie_contract,
    amel_commercial,
    base_event_data,
):
    marie_contract.sign_contract(updater_id=amel_commercial.id)
    contract_repository.create(marie_contract)

    event_data = {**base_event_data, "contract_id": marie_contract.id}

    auth_context = AuthContext(john_commercial)
    use_case = CreateEventUseCase(event_repository, contract_repository, uuid_generator, auth_context)

    with pytest.raises(PermissionError, match="You do not have permission to create an event for this contract"):
        use_case.execute(creator=john_commercial, **event_data)


def test_non_commercial_cannot_create_event(
    event_repository,
    contract_repository,
    bob_support,
    uuid_generator,
    karim_contract,
    base_event_data,
):
    karim_contract.sign_contract(updater_id=bob_support.id)
    contract_repository.create(karim_contract)

    event_data = {**base_event_data, "contract_id": karim_contract.id}

    auth_context = AuthContext(bob_support)
    use_case = CreateEventUseCase(event_repository, contract_repository, uuid_generator, auth_context)

    with pytest.raises(
        PermissionError,
        match=f"User '{bob_support.email}' with role '{bob_support.role.name.capitalize()}' does not have permission '{Permissions.CREATE_EVENT.name}'",
    ):
        use_case.execute(creator=bob_support, **event_data)


def test_commercial_cannot_create_event_with_date_end_lower_than_date_start(
    event_repository,
    contract_repository,
    john_commercial,
    uuid_generator,
    karim_contract,
    base_event_data,
):
    karim_contract.sign_contract(updater_id=john_commercial.id)
    contract_repository.create(karim_contract)

    # Set date_end earlier than date_start
    invalid_event_data = {
        **base_event_data,
        "contract_id": karim_contract.id,
        "date_end": base_event_data["date_start"] - timedelta(days=1),
    }

    auth_context = AuthContext(john_commercial)
    use_case = CreateEventUseCase(event_repository, contract_repository, uuid_generator, auth_context)

    with pytest.raises(ValueError, match="Event end date must be after start date"):
        use_case.execute(creator=john_commercial, **invalid_event_data)


def test_commercial_cannot_create_event_in_past(
    event_repository,
    contract_repository,
    john_commercial,
    uuid_generator,
    karim_contract,
    base_event_data,
):
    karim_contract.sign_contract(updater_id=john_commercial.id)
    contract_repository.create(karim_contract)

    past_date = datetime.now() - timedelta(days=10)
    invalid_event_data = {
        **base_event_data,
        "contract_id": karim_contract.id,
        "date_start": past_date,
        "date_end": past_date + timedelta(hours=8),
    }

    auth_context = AuthContext(john_commercial)
    use_case = CreateEventUseCase(event_repository, contract_repository, uuid_generator, auth_context)

    with pytest.raises(ValueError, match="Event start date must be in the future"):
        use_case.execute(creator=john_commercial, **invalid_event_data)
