import click

from collaborators.infrastructure.cli.services.session_manager import SessionManager
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)
from collaborators.infrastructure.security.password_hasher import BcryptPasswordHasher
from collaborators.tests.fakes.fake_password_hasher import FakePasswordHasher


@click.command("login")
@click.option("--email", prompt=True, help="Email")
@click.option("--password", prompt=True, hide_input=True, help="Password")
@click.pass_context
def login(ctx, email, password):
    """Authenticate and store a session token locally."""
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()

    # Use FakePasswordHasher in test env, BcryptPasswordHasher in production
    password_hasher = FakePasswordHasher() if (ctx.obj and ctx.obj.get("test_env")) else BcryptPasswordHasher()

    try:
        repo = SqlalchemyCollaboratorRepository(session)
        user = repo.find_by_email(email)

        if not user or not password_hasher.verify(password, user.password):
            click.echo("❌ Invalid email or password")
            return

        SessionManager.save_session({"id": user.id, "email": user.email, "role": user.role.value})
        click.echo(f"✅ Logged in as {user.first_name} {user.last_name}")

    except Exception as e:
        click.echo(f"❌ Error during login: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
