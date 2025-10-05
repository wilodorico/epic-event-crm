import click

from collaborators.application.contract.get_contracts_use_case import GetContractsUseCase
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository


@click.command(name="get-contracts", help="Retrieve and display all contracts")
@click.pass_context
@require_auth(Permissions.READ_CONTRACTS)
def get_contracts(ctx):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()
    auth_context = ctx.obj.get("auth_context")

    try:
        repository = SqlalchemyContractRepository(session)
        use_case = GetContractsUseCase(repository, auth_context)

        contracts = use_case.execute()

        if not contracts:
            click.echo("No contracts found.")
            return

        click.echo("List of Contracts:")
        for contract in contracts:
            click.echo(
                f"Contract_id : {contract.id} - Customer_id : {contract.customer_id} - "
                f"Total_amount : {contract.total_amount} - Remaining_amount : {contract.remaining_amount}"
            )

    except Exception as e:
        click.echo(f"❌ Error retrieving contracts: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
