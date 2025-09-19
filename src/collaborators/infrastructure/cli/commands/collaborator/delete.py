import click

from collaborators.application.collaborator.delete_collaborator_use_case import DeleteCollaboratorUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)
from commons.uuid_generator import UuidGenerator


@click.command("delete-collaborator")
@click.option("--id", "collaborator_id", prompt=True, type=str, help="ID of the collaborator to delete")
@click.pass_context
def delete_collaborator(ctx, collaborator_id: str):
    """
    Delete an existing by ID --id "<collaborator_id>".

    """
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()

    try:
        repository = SqlalchemyCollaboratorRepository(session)
        id_generator = UuidGenerator()
        existing_collaborator = repository.find_by_id(collaborator_id)
        if not existing_collaborator:
            click.echo(f"❌ Collaborator with ID '{collaborator_id}' not found.")
            return

        # TODO: Replace with proper authentication system
        temp_manager = Collaborator(
            id="cli-temp-manager",
            created_by_id="system",
            first_name="CLI",
            last_name="Manager",
            email="cli.manager@system.com",
            password="temp",
            phone_number="0000000000",
            role=Role.MANAGEMENT,
        )

        auth_context = AuthContext(temp_manager)
        use_case = DeleteCollaboratorUseCase(repository, id_generator, auth_context)
        use_case.execute(temp_manager, collaborator_id)

        click.echo(
            f"✅ Collaborator {existing_collaborator.first_name} {existing_collaborator.last_name} deleted successfully!"
        )
    except Exception as e:
        click.echo(f"❌ Error deleting collaborator: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
