from collaborators.application.event.get_support_events_use_case import GetSupportEventsUseCase
from collaborators.application.services.auth_context import AuthContext


def test_support_can_get_assigned_events(event_repository, manager_alice, bob_support, karim_event, marie_event):
    karim_event.assign_support(manager_alice.id, bob_support.id)
    event_repository.create(karim_event)
    event_repository.create(marie_event)

    auth_context = AuthContext(bob_support)
    use_case = GetSupportEventsUseCase(auth_context, event_repository)
    events = use_case.execute(bob_support.id)

    assert event_repository.count() == 2
    assert len(events) == 1
    assert events[0].title == karim_event.title
