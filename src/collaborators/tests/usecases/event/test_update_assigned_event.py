import pytest

from collaborators.application.event.update_assigned_event_use_case import UpdateAssignedEventUseCase
from collaborators.application.services.auth_context import AuthContext


def test_support_can_update_assigned_event(event_repository, manager_alice, bob_support, karim_event):
    karim_event.assign_support(manager_alice.id, bob_support.id)
    event_repository.create(karim_event)

    auth_context = AuthContext(bob_support)
    use_case = UpdateAssignedEventUseCase(auth_context, event_repository)
    updated_title = "Updated Event Title"
    updated_event = use_case.execute(
        event_id=karim_event.id,
        title=updated_title,
    )
    assert updated_event.title == updated_title
    assert updated_event.updated_by_id == bob_support.id
    assert updated_event.notes == karim_event.notes  # Unchanged field


def test_support_cannot_update_non_existent_event(event_repository, bob_support):
    auth_context = AuthContext(bob_support)
    use_case = UpdateAssignedEventUseCase(auth_context, event_repository)

    with pytest.raises(ValueError, match="Event not found"):
        use_case.execute(
            event_id=9999,  # Assuming this ID does not exist
            title="Should Fail",
        )


def test_support_cannot_update_unassigned_event(event_repository, manager_alice, bob_support, karim_event):
    # Event is not assigned to bob_support
    event_repository.create(karim_event)

    auth_context = AuthContext(bob_support)
    use_case = UpdateAssignedEventUseCase(auth_context, event_repository)

    with pytest.raises(PermissionError, match="Event not assigned to any support collaborator"):
        use_case.execute(
            event_id=karim_event.id,
            title="Should Fail",
        )
