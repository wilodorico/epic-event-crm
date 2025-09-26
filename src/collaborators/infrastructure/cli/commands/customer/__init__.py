import click

from collaborators.infrastructure.cli.commands.customer.create import create_customer
from collaborators.infrastructure.cli.commands.customer.get_customers import get_customers
from collaborators.infrastructure.cli.commands.customer.update import update_customer


@click.group()
def customer():
    """Related commands : tape --help for more details."""
    pass


customer.add_command(create_customer)
customer.add_command(update_customer)
customer.add_command(get_customers)
