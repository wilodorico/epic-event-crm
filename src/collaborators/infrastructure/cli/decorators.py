import functools
import os

import click

from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.services.session_manager import SessionManager
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)


def _is_test_mode() -> bool:
    return "PYTEST_CURRENT_TEST" in os.environ


def _load_user_from_context(ctx):
    return ctx.obj.get("current_user") if ctx.obj and "current_user" in ctx.obj else None


def _load_user_from_session():
    session_data = SessionManager.load_session()
    if not session_data:
        return None

    db = SessionLocal()
    try:
        repo = SqlalchemyCollaboratorRepository(db)
        return repo.find_by_id(session_data["id"])
    finally:
        db.close()


def _resolve_user(ctx):
    """Retrieve and inject the user into the context (test or prod)."""
    user = _load_user_from_context(ctx) if _is_test_mode() else _load_user_from_session()
    if user:
        if ctx.obj is None:
            ctx.obj = {}
        ctx.obj["current_user"] = user
    return user


def require_auth(permission: Permissions | None = None):
    """
    Checks authentication and optionally permission.
    - Prevents command execution if the user is not logged in.
    - Blocks Click prompts thanks to a hidden eager option.
    - Injects current_user and auth_context into ctx.obj.

    Usage:
        @click.command()
        @click.pass_context
        @require_auth(Permissions.CREATE_CUSTOMER)
        @click.option("--name", prompt=True)
        def my_command(ctx, name):
            ...
    """

    def decorator(f):
        def check_auth_callback(ctx, param, value):
            user = _resolve_user(ctx)

            if not user:
                click.echo("❌ You must login first")
                ctx.abort()

            auth_context = AuthContext(user)
            if permission and not auth_context.can(permission):
                click.echo("❌ You don't have permission to perform this action")
                ctx.abort()

            ctx.obj["auth_context"] = auth_context
            return value

        # Hidden option to perform this check before prompts
        f = click.option(
            "--auth-check",
            is_flag=True,
            default=True,
            hidden=True,
            expose_value=False,
            is_eager=True,
            callback=check_auth_callback,
        )(f)

        return functools.wraps(f)(f)

    return decorator
