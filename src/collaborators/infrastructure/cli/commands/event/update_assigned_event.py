import click

from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth


@click.command(name="update-assigned-event", help="Update an assigned event for the logged-in support collaborator")
@click.pass_context
@require_auth(Permissions.UPDATE_EVENT)
@click.option("--id", "event_id", required=True, help="ID of the event to update")
def update_assigned_event(ctx, event_id):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else None
    current_user = ctx.obj.get("current_user")
    auth_context = ctx.obj.get("auth_context")

    pass
