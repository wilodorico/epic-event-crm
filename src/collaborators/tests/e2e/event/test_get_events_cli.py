import pytest
from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.event import event
from collaborators.infrastructure.repositories.sqlalchemy_event_repository import SqlalchemyEventRepository


@pytest.mark.parametrize("collaborator_fixture", ["john_commercial", "manager_alice", "bob_support"])
def test_collaborator_get_events_cli(session, request, collaborator_fixture, karim_event):
    logged_user = request.getfixturevalue(collaborator_fixture)
    repo = SqlalchemyEventRepository(session)
    repo.create(karim_event)

    runner = CliRunner()
    result = runner.invoke(
        event,
        ["get-events"],
        obj={"session": session, "current_user": logged_user},
    )

    assert result.exit_code == 0
    assert "No events found." not in result.output
    assert "List of Events:" in result.output
    assert "Karim's Event" in result.output
