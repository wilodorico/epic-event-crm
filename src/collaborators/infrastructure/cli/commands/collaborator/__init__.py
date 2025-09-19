import click

from collaborators.infrastructure.cli.commands.collaborator.create import create_collaborator
from collaborators.infrastructure.cli.commands.collaborator.delete import delete_collaborator
from collaborators.infrastructure.cli.commands.collaborator.update import update_collaborator


@click.group()
def collaborator():
    """Related commands : tape --help for more details."""
    pass


collaborator.add_command(create_collaborator)
collaborator.add_command(update_collaborator)
collaborator.add_command(delete_collaborator)
