import click

from collaborators.infrastructure.cli.services.session_manager import SessionManager


@click.command("logout")
def logout():
    """
    Logout from the application.

    This command clears the current session by deleting the session file.
    After logout, you will need to login again to access protected commands.

    Example usage:
        $ python app.py auth logout
    """
    session_data = SessionManager.load_session()

    if not session_data:
        click.echo("❌ You are not logged in")
        return

    SessionManager.clear_session()
    click.echo("✅ Logged out successfully")
