import pytest

from collaborators.application.event.get_events_use_case import GetEventsUseCase
from collaborators.application.services.auth_context import AuthContext


@pytest.mark.parametrize("collaborator_fixture", ["john_commercial", "manager_alice", "bob_support"])
def test_collaborator_can_get_events(event_repository, request, collaborator_fixture):
    collaborator = request.getfixturevalue(collaborator_fixture)

    auth_context = AuthContext(collaborator)
    use_case = GetEventsUseCase(event_repository, auth_context)
    events = use_case.execute()

    assert event_repository.count() == 0
    assert events == []


@pytest.mark.parametrize("collaborator_fixture", ["john_commercial", "manager_alice", "bob_support"])
def test_collaborator_get_events_with_existing_events(
    event_repository, request, collaborator_fixture, karim_event, karim_contract
):
    collaborator = request.getfixturevalue(collaborator_fixture)
    karim_contract.sign_contract(updater_id=collaborator.id)
    event_repository.create(karim_event)

    auth_context = AuthContext(collaborator)
    use_case = GetEventsUseCase(event_repository, auth_context)
    events = use_case.execute()

    assert event_repository.count() == 1
    assert any(e.title == "Karim's Event" for e in events)
