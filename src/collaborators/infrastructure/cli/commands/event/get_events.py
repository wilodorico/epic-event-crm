import click

from collaborators.application.event.get_events_use_case import GetEventsUseCase
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_event_repository import SqlalchemyEventRepository


@click.command(name="get-events", help="Retrieve and display all events")
@click.pass_context
@require_auth(Permissions.READ_EVENTS)
def get_events(ctx):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()
    auth_context = ctx.obj.get("auth_context")

    try:
        repository = SqlalchemyEventRepository(session)
        use_case = GetEventsUseCase(repository, auth_context)

        events = use_case.execute()

        if not events:
            click.echo("No events found.")
            return

        click.echo("List of Events:")
        for event in events:
            click.echo(
                f"Event_id : {event.id} - Customer_id : {event.customer_id} - Contract_id : {event.contract_id} - "
                f"Title : {event.title} - Date_start : {event.date_start} - Date_end : {event.date_end} - "
                f"Location : {event.location} - Attendees : {event.attendees} - Notes : {event.notes}"
            )

    except Exception as e:
        click.echo(f"❌ Error retrieving events: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
