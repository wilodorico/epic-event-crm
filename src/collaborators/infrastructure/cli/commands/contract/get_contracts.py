import click

from collaborators.application.contract.get_contracts_use_case import GetContractsUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository


@click.command(name="get-contracts", help="Retrieve and display all contracts")
@click.pass_context
def get_contracts(ctx):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else None

    try:
        repository = SqlalchemyContractRepository(session)

        current_user = ctx.obj.get("current_user") if ctx.obj and "current_user" in ctx.obj else None

        if not current_user:
            current_user = Collaborator(
                id="cli-temp-manager",
                created_by_id="system",
                first_name="CLI",
                last_name="Manager",
                email="cli.manager@system.com",
                password="temp",
                phone_number="0000000000",
                role=Role.MANAGEMENT,
            )

        auth_context = AuthContext(current_user)
        use_case = GetContractsUseCase(repository, auth_context)

        contracts = use_case.execute()

        if not contracts:
            click.echo("No contracts found.")
            return

        click.echo("List of Contracts:")
        for contract in contracts:
            click.echo(f" - {contract.id}: {contract.customer_id} - {contract.total_amount}")

    except Exception as e:
        click.echo(f"❌ Error retrieving contracts: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
