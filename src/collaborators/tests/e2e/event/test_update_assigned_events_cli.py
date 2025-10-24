import pytest
from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.event import event
from collaborators.infrastructure.repositories.sqlalchemy_event_repository import SqlalchemyEventRepository


@pytest.mark.skip("Not totally implemented yet")
def test_support_can_update_assigned_event_cli(session, manager_alice, bob_support, karim_event):
    repo = SqlalchemyEventRepository(session)
    karim_event.assign_support(manager_alice.id, bob_support.id)
    repo.create(karim_event)
    logged_user = bob_support

    user_input = "Updated notes for the event.\n"  # Notes prompt

    runner = CliRunner()
    result = runner.invoke(
        event,
        ["update-assigned-event", "--id", karim_event.id],
        input=user_input,
        obj={"session": session, "current_user": logged_user},
    )

    assert result.exit_code == 0
    assert f"Event {karim_event.id} updated successfully" in result.output
