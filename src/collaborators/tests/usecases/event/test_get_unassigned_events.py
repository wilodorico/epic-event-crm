import pytest

from collaborators.application.event.get_unassigned_events_use_case import GetUnassignedEventsUseCase
from collaborators.application.services.auth_context import AuthContext


def test_manager_can_get_unassigned_events(event_repository, manager_alice, karim_event, karim_contract):
    karim_contract.sign_contract(updater_id=manager_alice.id)
    event_repository.create(karim_event)

    auth_context = AuthContext(manager_alice)
    use_case = GetUnassignedEventsUseCase(auth_context, event_repository)
    unassigned_events = use_case.execute()

    assert event_repository.count() == 1
    assert any(e.title == "Karim's Event" for e in unassigned_events)


def test_commercial_cannot_get_unassigned_events(event_repository, john_commercial):
    auth_context = AuthContext(john_commercial)
    use_case = GetUnassignedEventsUseCase(auth_context, event_repository)

    with pytest.raises(
        PermissionError,
        match=f"User '{john_commercial.email}' with role 'Commercial' does not have permission 'FILTER_EVENTS'",
    ):
        use_case.execute()
