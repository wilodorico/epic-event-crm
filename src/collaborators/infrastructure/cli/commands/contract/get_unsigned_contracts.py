import click

from collaborators.infrastructure.cli.decorators import require_auth


@click.command(name="get-unsigned-contracts", help="Retrieve and display all unsigned contracts")
@click.pass_context
@require_auth()
def get_unsigned_contracts(ctx):
    pass
