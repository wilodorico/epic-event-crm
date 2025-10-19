import click

from collaborators.application.collaborator.create_collaborator_use_case import CreateCollaboratorUseCase
from collaborators.domain.collaborator.collaborator import Role
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth
from collaborators.infrastructure.cli.inputs_validator import validate_email, validate_phone
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)
from collaborators.infrastructure.security.password_hasher import BcryptPasswordHasher
from commons.uuid_generator import UuidGenerator


@click.command("create-collaborator")
@click.pass_context
@require_auth(Permissions.CREATE_COLLABORATOR)
@click.option("--first-name", prompt=True, type=str)
@click.option("--last-name", prompt=True, type=str)
@click.option("--email", prompt=True, callback=validate_email)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@click.option("--phone-number", prompt=True, callback=validate_phone)
@click.option("--role", prompt=True, type=click.Choice([r.value for r in Role]))
def create_collaborator(ctx, first_name, last_name, email, password, phone_number, role):
    """
    Create a new collaborator.
    This command prompts for collaborator details and creates a new collaborator in the system.
    Example usage:
        $ python app.py collaborator create

    Prompts:
        - First Name
        - Last Name
        - Email
        - Password
        - Phone Number
        - Role (choices: Commercial, Management, Support)
    """
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()
    current_user = ctx.obj.get("current_user")
    auth_context = ctx.obj.get("auth_context")

    # TODO: Refactorer les try except finally avec un context manager
    try:
        repository = SqlalchemyCollaboratorRepository(session)
        id_generator = UuidGenerator()
        password_hasher = BcryptPasswordHasher()

        use_case = CreateCollaboratorUseCase(auth_context, repository, id_generator, password_hasher)
        # Convert string role to Role enum
        role_enum = Role(role)
        use_case.execute(
            creator=current_user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone_number=phone_number,
            role=role_enum,
        )
        click.echo(f"✅ Collaborator {first_name} {last_name} created!")
    except Exception as e:
        click.echo(f"❌ Error creating collaborator: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
