import click

from collaborators.infrastructure.cli.commands.event.assign_support_to_event import assign_support
from collaborators.infrastructure.cli.commands.event.create import create_event
from collaborators.infrastructure.cli.commands.event.get_events import get_events
from collaborators.infrastructure.cli.commands.event.get_my_events import get_my_events
from collaborators.infrastructure.cli.commands.event.get_unassigned_events import get_unassigned_events


@click.group()
def event():
    """Related commands : tape --help for more details."""
    pass


event.add_command(create_event)
event.add_command(get_events)
event.add_command(get_unassigned_events)
event.add_command(assign_support)
event.add_command(get_my_events)
