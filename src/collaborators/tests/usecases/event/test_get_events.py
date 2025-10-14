from collaborators.application.event.get_events_use_case import GetEventsUseCase
from collaborators.application.services.auth_context import AuthContext


def test_collaborator_can_get_events(event_repository, john_commercial):
    auth_context = AuthContext(john_commercial)
    use_case = GetEventsUseCase(event_repository, auth_context)
    events = use_case.execute()

    assert event_repository.count() == 0
    assert events == []


def test_collaborator_get_events_with_existing_events(event_repository, john_commercial, karim_event, karim_contract):
    karim_contract.sign_contract(updater_id=john_commercial.id)
    event_repository.create(karim_event)

    auth_context = AuthContext(john_commercial)
    use_case = GetEventsUseCase(event_repository, auth_context)
    events = use_case.execute()

    assert event_repository.count() == 1
    assert any(e.title == "Karim's Event" for e in events)
