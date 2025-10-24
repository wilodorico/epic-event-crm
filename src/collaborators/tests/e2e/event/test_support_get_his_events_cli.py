import pytest
from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.event import event
from collaborators.infrastructure.repositories.sqlalchemy_event_repository import SqlalchemyEventRepository


@pytest.mark.skip(reason="Not implemented yet")
def test_support_can_get_assigned_events_cli(session, manager_alice, bob_support, karim_event):
    repo = SqlalchemyEventRepository(session)
    repo.create(karim_event)
    karim_event.assign_support(manager_alice, bob_support)

    logged_user = bob_support

    runner = CliRunner()
    result = runner.invoke(
        event,
        ["get-my-events"],
        obj={"session": session, "current_user": logged_user},
    )

    assert result.exit_code == 0
    assert "No events found." not in result.output
    assert "List of Events:" in result.output
    assert "Karim's Event" in result.output
