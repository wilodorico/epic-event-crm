import click

from collaborators.application.event.get_support_events_use_case import GetSupportEventsUseCase
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth
from collaborators.infrastructure.repositories.sqlalchemy_event_repository import SqlalchemyEventRepository


@click.command(name="get-my-events", help="Retrieve and display events assigned to the logged-in support collaborator")
@click.pass_context
@require_auth(Permissions.READ_EVENTS)
def get_my_events(ctx):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else None
    current_user = ctx.obj.get("current_user")
    auth_context = ctx.obj.get("auth_context")

    try:
        repository = SqlalchemyEventRepository(session)
        use_case = GetSupportEventsUseCase(auth_context, repository)
        events = use_case.execute(current_user.id)

        if not events:
            click.echo("No events assigned to you.")
            return

        click.echo("Your Assigned Events:")
        for event in events:
            click.echo(
                f"Event_id : {event.id} - Customer_id : {event.customer_id} - Contract_id : {event.contract_id} - "
                f"Title : {event.title} - Date_start : {event.date_start} - Date_end : {event.date_end} - "
                f"Location : {event.location} - Attendees : {event.attendees} - Notes : {event.notes}"
            )

    except Exception as e:
        click.echo(f"❌ Error retrieving your events: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
