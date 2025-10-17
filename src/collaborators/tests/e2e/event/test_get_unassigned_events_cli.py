from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.event import event
from collaborators.infrastructure.repositories.sqlalchemy_event_repository import SqlalchemyEventRepository


def test_manager_can_get_unassigned_events_cli(session, manager_alice, karim_event):
    logged_user = manager_alice
    repo = SqlalchemyEventRepository(session)
    repo.create(karim_event)

    runner = CliRunner()
    result = runner.invoke(
        event,
        ["get-unassigned-events"],
        obj={"session": session, "current_user": logged_user},
    )

    assert result.exit_code == 0
    assert "No events found." not in result.output
    assert "List of unassigned Events:" in result.output
    assert "Karim's Event" in result.output
