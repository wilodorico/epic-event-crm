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


def _get_user_from_session():
    """
    Retrieves the user from the session file in production mode.

    In production mode, the user must authenticate via the 'login' command,
    which creates a session file. This function loads that session and
    checks that the user still exists in the database.

    Returns:
        Collaborator | None: The Collaborator object or None if not found/invalid
    """
    session_data = SessionManager.load_session()
    if not session_data:
        return None

    # Check that the user still exists in the database
    db = SessionLocal()
    try:
        repo = SqlalchemyCollaboratorRepository(db)
        user = repo.find_by_id(session_data["id"])
        return user
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


def require_permission(permission: Permissions):
    """
    Décorateur qui vérifie qu'un utilisateur a une permission spécifique avant d'exécuter une commande.

    Ce décorateur doit être placé immédiatement APRÈS @click.command() et AVANT @click.pass_context.
    Il intercepts l'exécution de la commande pour vérifier les permissions avant que
    Click ne commence à traiter les options avec prompt=True.

    Usage:
        @click.command()
        @require_permission(Permissions.CREATE_COLLABORATOR)
        @click.pass_context
        @require_login
        @click.option("--name", prompt=True)
        def my_command(ctx, name):
            pass

    Args:
        permission: La permission requise pour exécuter la commande

    Raises:
        click.Abort: Si l'utilisateur n'a pas la permission requise
    """

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            ctx = click.get_current_context()

            # @require_login devrait avoir déjà injecté current_user
            current_user = ctx.obj.get("current_user") if ctx.obj else None

            if not current_user:
                click.echo("❌ You must login first")
                ctx.abort()

            auth_context = AuthContext(current_user)
            if not auth_context.can(permission):
                click.echo("❌ You don't have permission to perform this action")
                ctx.abort()

            # Si les permissions sont OK, continuer
            return f(*args, **kwargs)

        return wrapper

    return decorator


def require_login_and_permission(permission: Permissions):
    """
    Décorateur combiné qui vérifie l'authentification ET les permissions avant les prompts.

    Ce décorateur combine @require_login et @require_permission en un seul pour garantir
    que les vérifications se font AVANT que Click ne traite les options avec prompt=True.

    Il utilise une option cachée avec is_eager=True et expose_value=False pour forcer
    l'évaluation des permissions avant tout autre traitement.

    Usage:
        @click.command()
        @click.pass_context
        @require_login_and_permission(Permissions.CREATE_COLLABORATOR)
        @click.option("--name", prompt=True)
        def my_command(ctx, name):
            pass

    Args:
        permission: La permission requise pour exécuter la commande

    Raises:
        click.Abort: Si l'utilisateur n'est pas connecté ou n'a pas la permission
    """

    def decorator(f):
        def check_permission_callback(ctx, param, value):
            """Callback exécuté en premier grâce à is_eager=True."""
            # Mode test : vérifier si l'utilisateur est dans le contexte
            if _is_test_mode():
                user = _get_user_from_test_context(ctx)
                if not user:
                    click.echo("❌ You must login first")
                    ctx.abort()

                # Injecter dans le contexte si pas déjà fait
                if ctx.obj is None:
                    ctx.obj = {}
                if "current_user" not in ctx.obj:
                    ctx.obj["current_user"] = user

                # Vérifier les permissions
                auth_context = AuthContext(user)
                if not auth_context.can(permission):
                    click.echo("❌ You don't have permission to perform this action")
                    ctx.abort()

                ctx.obj["auth_context"] = auth_context  # Injecter AuthContext pour usage ultérieur
                return value

            # Mode production : charger depuis la session
            user_data = _get_user_from_session()
            if not user_data:
                click.echo("❌ You must login first")
                ctx.abort()

            # Injecter dans le contexte
            if ctx.obj is None:
                ctx.obj = {}
            ctx.obj["current_user"] = user_data

            # Vérifier les permissions
            auth_context = AuthContext(user_data)
            if not auth_context.can(permission):
                click.echo("❌ You don't have permission to perform this action")
                ctx.abort()

            ctx.obj["auth_context"] = auth_context  # Injecter AuthContext pour usage ultérieur
            return value

        # Ajouter une option cachée eager qui force la vérification avant les prompts
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
