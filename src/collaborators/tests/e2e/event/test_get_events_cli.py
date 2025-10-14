import pytest
from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.event import event


@pytest.mark.skip(reason="To be implemented after event creation feature is complete")
def test_collaborator_get_events_cli(session, john_commercial):
    logged_user = john_commercial

    runner = CliRunner()
    result = runner.invoke(
        event,
        ["get-events"],
        obj={"session": session, "current_user": logged_user},
    )

    assert result.exit_code == 0
    assert "List of Events:" in result.output
