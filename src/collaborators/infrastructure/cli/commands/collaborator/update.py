import click

from collaborators.application.collaborator.update_collaborator_use_case import UpdateCollaboratorUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.cli.inputs_validator import validate_email, validate_phone
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)


@click.command("update-collaborator")
@click.option("--id", prompt=True, type=str, help="ID of the collaborator to update")
@click.pass_context
def update_collaborator(ctx, id):
    """
    Update an existing by ID --id "<collaborator_id>".
    The command will load the current data and allow you to modify each field.
    """
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()

    try:
        repository = SqlalchemyCollaboratorRepository(session)

        existing_collaborator = repository.find_by_id(id)
        if not existing_collaborator:
            click.echo(f"❌ Collaborator with ID '{id}' not found.")
            return

        click.echo(f"Updating collaborator: {existing_collaborator.first_name} {existing_collaborator.last_name}")
        click.echo("Press Enter to keep current value, or type new value:")
        click.echo()

        first_name = click.prompt("First name", default=existing_collaborator.first_name, show_default=True)
        last_name = click.prompt("Last name", default=existing_collaborator.last_name, show_default=True)
        email = click.prompt("Email", default=existing_collaborator.email, show_default=True)
        try:
            validate_email(None, None, email)
        except click.BadParameter as e:
            click.echo(f"❌ {e}")
            return

        phone_number = click.prompt("Phone number", default=existing_collaborator.phone_number, show_default=True)
        try:
            validate_phone(None, None, phone_number)
        except click.BadParameter as e:
            click.echo(f"❌ {e}")
            return

        role = click.prompt(
            "Role",
            default=existing_collaborator.role.value,
            show_default=True,
            type=click.Choice([r.value for r in Role]),
        )

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
        use_case = UpdateCollaboratorUseCase(repository, auth_context)

        # Prepare update data (only include changed fields)
        update_data = {}
        if first_name != existing_collaborator.first_name:
            update_data["first_name"] = first_name
        if last_name != existing_collaborator.last_name:
            update_data["last_name"] = last_name
        if email != existing_collaborator.email:
            update_data["email"] = email
        if phone_number != existing_collaborator.phone_number:
            update_data["phone_number"] = phone_number
        if Role(role) != existing_collaborator.role:
            update_data["role"] = Role(role)

        if not update_data:
            click.echo("No changes detected. Collaborator not updated.")
            return

        updated_collaborator = use_case.execute(temp_manager, id, update_data)
        click.echo(
            f"✅ Collaborator {updated_collaborator.first_name} {updated_collaborator.last_name} updated successfully!"
        )

    except Exception as e:
        click.echo(f"❌ Error updating collaborator: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
