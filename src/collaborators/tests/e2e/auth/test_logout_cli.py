from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.auth import auth
from collaborators.infrastructure.cli.services.session_manager import SessionManager
from collaborators.infrastructure.security.jwt_service import JWTService


def test_logout_cli(session, john_commercial):
    logged_user = john_commercial
    jwt_service = JWTService()

    token = jwt_service.encode(
        {
            "id": logged_user.id,
            "email": logged_user.email,
            "role": logged_user.role.value,
        }
    )

    SessionManager.save_session({"token": token})

    runner = CliRunner()
    result = runner.invoke(
        auth,
        ["logout"],
        obj={"session": session, "current_user": logged_user},
    )

    assert result.exit_code == 0
    assert "✅ Logged out successfully" in result.output
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
