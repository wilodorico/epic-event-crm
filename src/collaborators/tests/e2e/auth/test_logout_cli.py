from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.auth import auth
from collaborators.infrastructure.cli.services.session_manager import SessionManager


def test_logout_cli(session, john_commercial):
    logged_user = john_commercial

    # Create a session file to simulate a logged-in user
    SessionManager.save_session(
        {
            "user_id": logged_user.id,
            "email": logged_user.email,
            "first_name": logged_user.first_name,
            "last_name": logged_user.last_name,
            "role": logged_user.role.value,
        }
    )

    runner = CliRunner()
    result = runner.invoke(
        auth,
        ["logout"],
        obj={"session": session, "current_user": logged_user},
    )

    assert result.exit_code == 0
    assert "✅ Logged out successfully" in result.output

    # Verify the session file has been deleted
    assert SessionManager.load_session() is None


def test_logout_not_logged_in_cli(session):
    runner = CliRunner()
    result = runner.invoke(
        auth,
        ["logout"],
        obj={"session": session, "current_user": None},
    )

    assert result.exit_code == 0
    assert "❌ You are not logged in" in result.output
