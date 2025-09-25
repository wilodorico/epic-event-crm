import click

from collaborators.infrastructure.cli.commands.collaborator import collaborator
from collaborators.infrastructure.cli.commands.contract import contract
from collaborators.infrastructure.cli.commands.customer import customer
from collaborators.infrastructure.cli.commands.init_db import init_db_command


@click.group()
def cli():
    """CRM CLI Application"""
    pass


cli.add_command(init_db_command)
cli.add_command(collaborator)
cli.add_command(customer)
cli.add_command(contract)
