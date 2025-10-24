import click

from collaborators.application.event.update_assigned_event_use_case import UpdateAssignedEventUseCase
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth
from collaborators.infrastructure.repositories.sqlalchemy_event_repository import SqlalchemyEventRepository


@click.command(name="update-assigned-event", help="Update an assigned event for the logged-in support collaborator")
@click.pass_context
@require_auth(Permissions.UPDATE_EVENT)
@click.option("--id", "event_id", required=True, help="ID of the event to update")
def update_assigned_event(ctx, event_id):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else None
    auth_context = ctx.obj.get("auth_context")

    try:
        repository = SqlalchemyEventRepository(session)

        existing_event = repository.find_by_id(event_id)
        if not existing_event:
            click.echo(f"❌ Event with ID '{event_id}' not found.")
            return

        click.echo(f"Updating event: {existing_event.title}")
        click.echo("Press Enter to keep current value, or type new value:")
        click.echo()

        title = click.prompt("Title", default=existing_event.title, show_default=True)
        date_start = click.prompt(
            "Start Date (YYYY-MM-DD HH:MM)",
            default=existing_event.date_start.strftime("%Y-%m-%d %H:%M"),
            type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),
            show_default=True,
        )
        date_end = click.prompt(
            "End Date (YYYY-MM-DD HH:MM)",
            default=existing_event.date_end.strftime("%Y-%m-%d %H:%M"),
            type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),
            show_default=True,
        )
        location = click.prompt("Location", default=existing_event.location, show_default=True)
        attendees = click.prompt("Attendees", default=existing_event.attendees, show_default=True)
        notes = click.prompt("Notes", default=existing_event.notes, show_default=True)

        use_case = UpdateAssignedEventUseCase(auth_context, repository)

        update_data = {}
        if title != existing_event.title:
            update_data["title"] = title
        if date_start != existing_event.date_start:
            update_data["date_start"] = date_start
        if date_end != existing_event.date_end:
            update_data["date_end"] = date_end
        if location != existing_event.location:
            update_data["location"] = location
        if attendees != existing_event.attendees:
            update_data["attendees"] = attendees
        if notes != existing_event.notes:
            update_data["notes"] = notes

        if not update_data:
            click.echo("No changes detected. Event not updated.")
            return

        updated_event = use_case.execute(event_id, **update_data)

        click.echo(f"✅ Event updated successfully: {updated_event.title}")

    except Exception as e:
        click.echo(f"❌ Error updating event: {e}")
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
