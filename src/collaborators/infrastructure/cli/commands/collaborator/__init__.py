import click

from collaborators.infrastructure.cli.commands.collaborator.create import create_collaborator


@click.group()
def collaborator():
    """Collaborator related commands."""
    pass


collaborator.add_command(create_collaborator)
