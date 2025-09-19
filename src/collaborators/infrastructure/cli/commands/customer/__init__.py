import click

from collaborators.infrastructure.cli.commands.customer.create import create_customer


@click.group()
def customer():
    """Related commands : tape --help for more details."""
    pass


customer.add_command(create_customer)
