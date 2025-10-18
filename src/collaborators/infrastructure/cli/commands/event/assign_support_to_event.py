import click

from collaborators.application.event.assign_support_to_event_use_case import AssignSupportToEventUseCase
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth
from collaborators.infrastructure.repositories.sqlalchemy_event_repository import SqlalchemyEventRepository


@click.command(name="assign-support", help="Assign a support collaborator to an event")
@click.pass_context
@require_auth(Permissions.READ_EVENTS)
@click.option("--event-id", prompt="Event ID", type=str, help="ID of the event to assign support to")
@click.option("--support-id", prompt="Support ID", type=str, help="ID of the support collaborator")
def assign_support(ctx, event_id, support_id):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else None
    auth_context = ctx.obj.get("auth_context")
    current_user = ctx.obj.get("current_user")

    try:
        repository = SqlalchemyEventRepository(session)
        use_case = AssignSupportToEventUseCase(repository, auth_context)
        event = use_case.execute(current_user, event_id, support_id)
        click.echo(f"✅ Support assigned to '{event.title}' successfully.")
    except Exception as e:
        click.echo(f"❌ Error assigning support to event: {str(e)}")
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
