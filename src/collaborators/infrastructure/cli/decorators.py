import functools
import os

import click

from collaborators.infrastructure.cli.services.session_manager import SessionManager
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)


def require_login(f):
    """Décorateur qui vérifie si l'utilisateur est connecté avant d'exécuter une commande."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context()

        # Vérifier si on est en mode test via variable d'environnement pytest
        # pytest définit automatiquement la variable PYTEST_CURRENT_TEST
        is_test_mode = "PYTEST_CURRENT_TEST" in os.environ

        # En mode test, si un utilisateur est fourni dans le contexte, l'utiliser directement
        if is_test_mode and ctx.obj and "current_user" in ctx.obj:
            return f(*args, **kwargs)

        # Mode production : vérifier le fichier de session
        session_data = SessionManager.load_session()
        if not session_data:
            click.echo("❌ You must login first")
            return

        # Charger l'utilisateur depuis la base de données
        db_session = SessionLocal()
        session_created_locally = False

        try:
            repo = SqlalchemyCollaboratorRepository(db_session)
            user = repo.find_by_id(session_data["id"])
            if not user:
                click.echo("❌ Invalid session. Please login again.")
                SessionManager.clear_session()
                return

            # Injecter l'utilisateur dans le contexte Click
            if ctx.obj is None:
                ctx.obj = {}
            ctx.obj["current_user"] = user

            # Ne créer une session que si elle n'existe pas déjà dans le contexte
            if "session" not in ctx.obj:
                ctx.obj["session"] = db_session
                session_created_locally = True

            return f(*args, **kwargs)
        finally:
            # Fermer la session seulement si elle a été créée localement
            if session_created_locally:
                db_session.close()

    return wrapper
