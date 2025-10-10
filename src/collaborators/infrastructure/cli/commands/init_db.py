import click

from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.database.db import SessionLocal, init_db
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)
from collaborators.infrastructure.security.password_hasher import BcryptPasswordHasher


@click.command("init-db")
def init_db_command():
    """Initialize the database and create default data."""
    click.echo("🧱 Initializing database...")
    init_db()

    session = SessionLocal()
    try:
        repo = SqlalchemyCollaboratorRepository(session)
        password_hasher = BcryptPasswordHasher()

        existing_manager = repo.find_by_email("admin@crm.com")
        if existing_manager:
            click.echo("ℹ️ Default manager already exists.")
            return

        manager = Collaborator(
            id="default-manager",
            created_by_id="system",
            first_name="Admin",
            last_name="Manager",
            email="admin@crm.com",
            password=password_hasher.hash("admin"),
            phone_number="0000000000",
            role=Role.MANAGEMENT,
        )

        repo.create(manager)
        session.commit()

        click.echo("👑 Default manager created:")
        click.echo("   Email: admin@crm.com")
        click.echo("   Password: admin")
        click.echo("   Role: MANAGEMENT")

    except Exception as e:
        click.echo(f"❌ Error creating default manager: {str(e)}")
        raise
    finally:
        session.close()
