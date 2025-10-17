import click

from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth


@click.command(name="assign-support", help="Assign a support collaborator to an event")
@click.pass_context
@require_auth(Permissions.READ_EVENTS)
def assign_support(ctx):
    pass
