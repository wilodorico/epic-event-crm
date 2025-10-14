import click

from collaborators.infrastructure.cli.commands.event.create import create_event
from collaborators.infrastructure.cli.commands.event.get_events import get_events


@click.group()
def event():
    """Related commands : tape --help for more details."""
    pass


event.add_command(create_event)
event.add_command(get_events)
