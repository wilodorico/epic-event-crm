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
    """Detecte si l’application est exécutée en mode test (pytest)."""
    return "PYTEST_CURRENT_TEST" in os.environ


def _load_user_from_context(ctx) -> object | None:
    """Récupère l'utilisateur injecté dans le contexte Click pendant les tests."""
    return ctx.obj.get("current_user") if ctx.obj and "current_user" in ctx.obj else None


def _load_user_from_session() -> object | None:
    """Charge l'utilisateur depuis le fichier de session (production)."""
    session_data = SessionManager.load_session()
    if not session_data:
        return None

    db = SessionLocal()
    try:
        repo = SqlalchemyCollaboratorRepository(db)
        user = repo.find_by_id(session_data["id"])
        return user
    finally:
        db.close()


def _resolve_current_user(ctx):
    """
    Récupère l'utilisateur (depuis le contexte test ou la session persistée)
    et l’injecte dans le contexte Click si nécessaire.
    """
    user = _load_user_from_context(ctx) if _is_test_mode() else _load_user_from_session()
    if user:
        if ctx.obj is None:
            ctx.obj = {}
        ctx.obj["current_user"] = user
    return user


def _has_permission(user, permission: Permissions) -> bool:
    """Retourne True si l'utilisateur possède la permission donnée."""
    if not user:
        return False
    return AuthContext(user).can(permission)


def get_current_user(ctx):
    """Récupère l'utilisateur courant injecté dans le contexte."""
    if not ctx.obj or "current_user" not in ctx.obj:
        raise click.ClickException("❌ No authenticated user found.")
    return ctx.obj["current_user"]


def get_auth_context(ctx) -> AuthContext:
    """Récupère (ou crée) l'AuthContext courant depuis le contexte Click."""
    user = get_current_user(ctx)
    if "auth_context" not in ctx.obj:
        ctx.obj["auth_context"] = AuthContext(user)
    return ctx.obj["auth_context"]


def require_login(f):
    """
    Vérifie que l'utilisateur est connecté avant d'exécuter une commande.
    Gère à la fois le mode test (pytest) et le mode production (session persistée).
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        user = _resolve_current_user(ctx)

        if not user:
            click.echo("❌ You must login first")
            return

        return f(*args, **kwargs)

    return wrapper


def require_permission(permission: Permissions):
    """
    Vérifie qu’un utilisateur a une permission spécifique avant d’exécuter la commande.
    Doit être placé **après @require_login**.
    """

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            ctx = click.get_current_context()
            current_user = ctx.obj.get("current_user") if ctx.obj else None

            if not current_user:
                click.echo("❌ You must login first")
                ctx.abort()

            if not _has_permission(current_user, permission):
                click.echo("❌ You don't have permission to perform this action")
                ctx.abort()

            return f(*args, **kwargs)

        return wrapper

    return decorator


def require_login_and_permission(permission: Permissions):
    """
    Combine login + permission check avant tout prompt Click.
    Garantit que les vérifications s’exécutent AVANT que Click ne demande des entrées à l'utilisateur.
    """

    def decorator(f):
        def check_permission_callback(ctx, param, value):
            """Callback exécuté en premier grâce à is_eager=True."""
            user = _resolve_current_user(ctx)

            if not user:
                click.echo("❌ You must login first")
                ctx.abort()

            if not _has_permission(user, permission):
                click.echo("❌ You don't have permission to perform this action")
                ctx.abort()

            ctx.obj["auth_context"] = AuthContext(user)
            return value

        f = click.option(
            "--auth-check",
            is_flag=True,
            default=True,
            hidden=True,
            expose_value=False,
            is_eager=True,
            callback=check_permission_callback,
        )(f)

        return f

    return decorator
