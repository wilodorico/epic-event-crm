import click

from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth


@click.command(name="get-my-events", help="Retrieve and display events assigned to the logged-in support collaborator")
@click.pass_context
@require_auth(Permissions.READ_EVENTS)
def get_my_events(ctx):
    pass
