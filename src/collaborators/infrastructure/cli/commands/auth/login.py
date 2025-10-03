import click

from collaborators.infrastructure.cli.services.session_manager import SessionManager
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)


@click.command("login")
@click.option("--email", prompt=True, help="Email")
@click.option("--password", prompt=True, hide_input=True, help="Password")
@click.pass_context
def login(ctx, email, password):
    """Authenticate and store a session token locally."""
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()

    try:
        repo = SqlalchemyCollaboratorRepository(session)
        user = repo.find_by_email(email)

        if not user or user.password != password:  # ⚠️ plus tard: hash
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
