from datetime import datetime

import pytest

from collaborators.application.event.create_event_use_case import CreateEventUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.contract.contract import ContractStatus


def test_commercial_can_create_event(
    event_repository, contract_repository, john_commercial, uuid_generator, karim_contract
):
    karim_contract.sign_contract(updater_id=john_commercial.id)
    contract_repository.create(karim_contract)
    date_start = datetime(2025, 12, 15, 9, 0, 0)
    date_end = datetime(2025, 12, 15, 17, 0, 0)
    attendees = 150

    event_data = {
        "title": "Annual Meeting",
        "contract_id": karim_contract.id,
        "date_start": date_start,
        "date_end": date_end,
        "location": "Main Conference Hall",
        "attendees": attendees,
        "notes": "Bring your ID for entry",
    }

    auth_context = AuthContext(john_commercial)
    use_case = CreateEventUseCase(event_repository, contract_repository, uuid_generator, auth_context)
    created_event = use_case.execute(creator=john_commercial, **event_data)

    assert karim_contract.status == ContractStatus.SIGNED
    assert created_event.id is not None
    assert created_event.title == "Annual Meeting"
    assert created_event.customer_id == karim_contract.customer_id
    assert created_event.contract_id == karim_contract.id
    assert created_event.date_start == date_start
    assert created_event.date_end == date_end
    assert created_event.location == "Main Conference Hall"
    assert created_event.attendees == attendees
    assert created_event.notes == "Bring your ID for entry"


def test_commercial_cannot_create_event_if_contract_not_signed(
    event_repository, contract_repository, john_commercial, uuid_generator, karim_contract
):
    contract_repository.create(karim_contract)
    date_start = datetime(2025, 12, 15, 9, 0, 0)
    date_end = datetime(2025, 12, 15, 17, 0, 0)
    attendees = 150

    event_data = {
        "title": "Annual Meeting",
        "contract_id": karim_contract.id,
        "date_start": date_start,
        "date_end": date_end,
        "location": "Main Conference Hall",
        "attendees": attendees,
        "notes": "Bring your ID for entry",
    }

    auth_context = AuthContext(john_commercial)
    use_case = CreateEventUseCase(event_repository, contract_repository, uuid_generator, auth_context)

    with pytest.raises(ValueError, match="Contract must be signed to create an event"):
        use_case.execute(creator=john_commercial, **event_data)


def test_commercial_cannot_create_event_with_non_existent_contract(
    event_repository, contract_repository, john_commercial, uuid_generator
):
    date_start = datetime(2025, 12, 15, 9, 0, 0)
    date_end = datetime(2025, 12, 15, 17, 0, 0)
    attendees = 150

    event_data = {
        "title": "Annual Meeting",
        "contract_id": "non-existent-contract-id",
        "date_start": date_start,
        "date_end": date_end,
        "location": "Main Conference Hall",
        "attendees": attendees,
        "notes": "Bring your ID for entry",
    }

    auth_context = AuthContext(john_commercial)
    use_case = CreateEventUseCase(event_repository, contract_repository, uuid_generator, auth_context)

    with pytest.raises(ValueError, match="Contract not found"):
        use_case.execute(creator=john_commercial, **event_data)
