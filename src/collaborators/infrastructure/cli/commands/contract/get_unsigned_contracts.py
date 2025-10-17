import click

from collaborators.application.contract.get_unsigned_contracts_use_case import GetUnsignedContractsUseCase
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository


@click.command(name="get-unsigned-contracts", help="Retrieve and display all unsigned contracts")
@click.pass_context
@require_auth(Permissions.FILTER_CONTRACTS)
def get_unsigned_contracts(ctx):
    """CLI command to get all unsigned contracts of the commercial."""
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()
    current_user = ctx.obj.get("current_user")
    auth_context = ctx.obj.get("auth_context")

    try:
        repository = SqlalchemyContractRepository(session)
        use_case = GetUnsignedContractsUseCase(repository, auth_context)

        unsigned_contracts = use_case.execute(current_user.id)

        if not unsigned_contracts:
            click.echo("No unsigned contracts found.")
            return

        click.echo("List of Unsigned Contracts:")
        for contract in unsigned_contracts:
            click.echo(
                f"Contract_id : {contract.id} - Customer_id : {contract.customer_id} - "
                f"Total_amount : {contract.total_amount} - Remaining_amount : {contract.remaining_amount}"
            )

    except Exception as e:
        click.echo(f"❌ Error retrieving unsigned contracts: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
