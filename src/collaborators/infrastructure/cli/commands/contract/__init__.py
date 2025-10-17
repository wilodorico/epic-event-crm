import click

from collaborators.infrastructure.cli.commands.contract.create import create_contract
from collaborators.infrastructure.cli.commands.contract.get_contracts import get_contracts
from collaborators.infrastructure.cli.commands.contract.get_unpaid_contracts import get_unpaid_contracts
from collaborators.infrastructure.cli.commands.contract.get_unsigned_contracts import get_unsigned_contracts
from collaborators.infrastructure.cli.commands.contract.sign_contract import sign_contract
from collaborators.infrastructure.cli.commands.contract.update import update_contract


@click.group()
def contract():
    """Related commands : tape --help for more details."""
    pass


contract.add_command(create_contract)
contract.add_command(update_contract)
contract.add_command(get_contracts)
contract.add_command(get_unsigned_contracts)
contract.add_command(get_unpaid_contracts)
contract.add_command(sign_contract)
