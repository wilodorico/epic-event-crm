import click

from collaborators.application.event.create_event_use_case import CreateEventUseCase
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth
from collaborators.infrastructure.cli.inputs_validator import validate_date_end, validate_date_start
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository
from collaborators.infrastructure.repositories.sqlalchemy_event_repository import SqlalchemyEventRepository
from commons.uuid_generator import UuidGenerator


@click.command("create")
@click.pass_context
@require_auth(Permissions.CREATE_EVENT)
@click.option("--contract-id", prompt=True, type=str, help="ID of the contract to associate the event with")
@click.option("--title", prompt=True, type=str, help="Title of the event")
@click.option(
    "--date-start",
    prompt=True,
    type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),
    callback=validate_date_start,
    help="Start date and time of the event (format: YYYY-MM-DD HH:MM)",
)
@click.option(
    "--date-end",
    prompt=True,
    type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),
    callback=validate_date_end,
    help="End date and time of the event (format: YYYY-MM-DD HH:MM)",
)
@click.option("--location", prompt=True, type=str, help="Location of the event")
@click.option("--attendees", prompt=True, type=click.INT, help="Number of attendees")
@click.option("--notes", prompt=True, type=str, help="Additional notes about the event")
def create_event(ctx, contract_id, title, date_start, date_end, location, attendees, notes):
    """
    Create a new event for a contract.
    This command creates a new event associated with a specified contract in the system.
    Example usage:
        $ python app.py event create --contract-id <contract_id> --title <title> --date-start <date_start> --date-end <date_end> --location <location> --attendees <attendees> --notes <notes>
    Arguments:
        - contract_id: ID of the contract to associate the event with
        - title: Title of the event
        - date_start: Start date and time of the event
        - date_end: End date and time of the event
        - location: Location of the event
        - attendees: Number of attendees
        - notes: Additional notes about the event
    """
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()
    current_user = ctx.obj.get("current_user")
    auth_context = ctx.obj.get("auth_context")

    try:
        repository = SqlalchemyEventRepository(session)
        contract_repository = SqlalchemyContractRepository(session)
        uuid_generator = UuidGenerator()

        use_case = CreateEventUseCase(repository, contract_repository, uuid_generator, auth_context)
        event = use_case.execute(
            creator=current_user,
            contract_id=contract_id,
            title=title,
            date_start=date_start,
            date_end=date_end,
            location=location,
            attendees=attendees,
            notes=notes,
        )

        click.echo(f"✅ Event {event.title} created successfully with ID: {event.id}")
    except Exception as e:
        click.echo(f"❌ Error creating event: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
