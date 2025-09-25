import click

from collaborators.infrastructure.cli.commands.contract.create import create_contract


@click.group()
def contract():
    """Related commands : tape --help for more details."""
    pass


contract.add_command(create_contract)
