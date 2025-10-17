import click

from collaborators.infrastructure.cli.decorators import require_auth


@click.command(name="get-unassigned-events", help="Retrieve and display all unassigned events")
@click.pass_context
@require_auth()
def get_unassigned_events(ctx):
    pass
