import click

from collaborators.infrastructure.cli.commands.event.create import create_event


@click.group()
def event():
    """Related commands : tape --help for more details."""
    pass


event.add_command(create_event)
