import click

from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth


@click.command(name="get-unpaid-contracts", help="Retrieve and display all unpaid contracts")
@click.pass_context
@require_auth(Permissions.FILTER_CONTRACTS)
def get_unpaid_contracts(ctx):
    """CLI command to get all unpaid contracts of the commercial."""
    pass
