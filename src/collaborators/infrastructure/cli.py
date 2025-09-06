import click

from collaborators.application.collaborator.create_collaborator_use_case import CreateCollaboratorUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.database.db import SessionLocal, init_db
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)
from commons.uuid_generator import UuidGenerator


@click.group()
def cli():
    """CRM CLI Application"""
    pass


@cli.command("init-db")
def init_db_command():
    """Initialize the database."""
    init_db()
    click.echo("✅ Database initialized!")


@cli.command("create-collaborator")
@click.option("--first-name", prompt=True)
@click.option("--last-name", prompt=True)
@click.option("--email", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@click.option("--phone-number", prompt=True)
@click.option("--role", prompt=True, type=click.Choice([r.value for r in Role]))
def create_collaborator(first_name, last_name, email, password, phone_number, role):
    """Create a new collaborator."""
    session = SessionLocal()
    try:
        repository = SqlalchemyCollaboratorRepository(session)
        id_generator = UuidGenerator()

        alice_manager = Collaborator(
            id="alice-manager-1",
            created_by_id="system-admin-1",
            first_name="Alice",
            last_name="Merveille",
            email="alice.merveille@gmail.com",
            password="securepassword",
            phone_number="0601010101",
            role=Role.MANAGEMENT,
        )

        auth_context = AuthContext(alice_manager)

        use_case = CreateCollaboratorUseCase(repository, id_generator, auth_context)
        use_case.execute(
            creator=alice_manager,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone_number=phone_number,
            role=role,
        )
    finally:
        session.close()
    click.echo(f"✅ Collaborator {first_name} {last_name} created!")
