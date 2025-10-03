import functools
import os

import click

from collaborators.infrastructure.cli.services.session_manager import SessionManager
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)


def _is_test_mode() -> bool:
    """
    Checks if the code is running in a test context.

    pytest automatically sets the environment variable PYTEST_CURRENT_TEST
    when running tests, which allows us to reliably detect test mode.

    Returns:
        bool: True if in test mode, False otherwise
    """
    return "PYTEST_CURRENT_TEST" in os.environ


def _get_user_from_test_context(ctx) -> dict | None:
    """
    Retrieves the user from the Click context in test mode.

    In test mode, the user is injected directly into the Click context
    via ctx.obj["current_user"] by pytest fixtures.

    Args:
        ctx: The Click context

    Returns:
        dict | None: The user data or None if not found
    """
    if ctx.obj and "current_user" in ctx.obj:
        return ctx.obj["current_user"]
    return None


def _get_user_from_session() -> dict | None:
    """
    Retrieves the user from the session file in production mode.

    In production mode, the user must authenticate via the 'login' command,
    which creates a session file. This function loads that session and
    checks that the user still exists in the database.

    Returns:
        dict | None: The user data or None if not found/invalid
    """
    session_data = SessionManager.load_session()
    if not session_data:
        return None

    # Check that the user still exists in the database
    db = SessionLocal()
    try:
        repo = SqlalchemyCollaboratorRepository(db)
        user = repo.get_by_id(session_data["id"])
        if user:
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            }
        return None
    finally:
        db.close()


def require_login(f):
    """
    Decorator that checks if the user is logged in before executing a command.

    This decorator handles two authentication modes:
    - Test mode: The user is injected into the Click context by fixtures
    - Production mode: The user must log in via 'login' (session file)

    The decorator ensures that after its execution, ctx.obj["current_user"] always contains
    a valid user, allowing commands to assume that current_user is present without further checks.
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context()

        # Test mode: use the user from the context if available
        if _is_test_mode():
            user = _get_user_from_test_context(ctx)
            if user:
                return f(*args, **kwargs)

        # Production mode: load the user from the session
        user_data = _get_user_from_session()
        if not user_data:
            click.echo("❌ You must login first")
            return

        # Inject the user into the Click context
        if ctx.obj is None:
            ctx.obj = {}
        ctx.obj["current_user"] = user_data

        return f(*args, **kwargs)

    return wrapper
