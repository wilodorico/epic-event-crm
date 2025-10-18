import pytest

from collaborators.application.event.assign_support_to_event_use_case import AssignSupportToEventUseCase
from collaborators.application.services.auth_context import AuthContext


def test_manager_can_assign_support_to_event(
    event_repository, manager_alice, bob_support, karim_event, karim_contract
):
    karim_contract.sign_contract(updater_id=manager_alice.id)
    event_repository.create(karim_event)

    auth_context = AuthContext(manager_alice)
    use_case = AssignSupportToEventUseCase(event_repository, auth_context)
    assigned_event = use_case.execute(collaborator=manager_alice, event_id=karim_event.id, support_id=bob_support.id)

    assert event_repository.count() == 1
    assert assigned_event.contact_support_id is not None
    assert assigned_event.contact_support_id == bob_support.id


def test_non_manager_cannot_assign_support_to_event(event_repository, john_commercial):
    auth_context = AuthContext(john_commercial)
    use_case = AssignSupportToEventUseCase(event_repository, auth_context)

    with pytest.raises(
        PermissionError,
        match=f"User '{john_commercial.email}' with role 'Commercial' does not have permission 'ASSIGN_EVENT'",
    ):
        use_case.execute(collaborator=john_commercial, event_id="some_event_id", support_id="some_support_id")


def test_manager_cannot_assign_support_to_non_existent_event(event_repository, manager_alice, bob_support):
    auth_context = AuthContext(manager_alice)
    use_case = AssignSupportToEventUseCase(event_repository, auth_context)

    with pytest.raises(ValueError, match="Event not found."):
        use_case.execute(collaborator=manager_alice, event_id="non_existent_event_id", support_id=bob_support.id)
