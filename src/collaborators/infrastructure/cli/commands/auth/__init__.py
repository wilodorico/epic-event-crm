import click

from collaborators.infrastructure.cli.commands.auth.login import login


@click.group()
def auth():
    """Authentication related commands: tape --help for more details."""
    pass


auth.add_command(login)
