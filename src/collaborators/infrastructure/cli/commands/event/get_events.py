import click

from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth


@click.command(name="get-events", help="Retrieve and display all events")
@click.pass_context
@require_auth(Permissions.READ_EVENTS)
def get_events():
    pass
