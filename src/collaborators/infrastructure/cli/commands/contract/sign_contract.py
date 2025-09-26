import click

from collaborators.application.contract.sign_contract_use_case import SignContractUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.domain.contract.contract import ContractStatus
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository


@click.command("sign-contract")
@click.option("--id", prompt="Contract ID", type=str, help="ID of the contract to sign")
@click.pass_context
def sign_contract(ctx, id):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()

    try:
        contract_repository = SqlalchemyContractRepository(session)

        existing_contract = contract_repository.find_by_id(id)
        if not existing_contract:
            click.echo(f"❌ Contract with ID '{id}' not found.")
            return

        if existing_contract.status == ContractStatus.SIGNED:
            click.echo(f"❌ Contract with ID '{id}' is already signed.")
            return

        confirm = click.prompt(f"Are you sure you want to sign contract '{id}'? (yes/no)", type=str)
        if confirm.lower() != "yes":
            click.echo("Signing operation cancelled.")
            return

        # Get user from context (for tests) or use default
        current_user = ctx.obj.get("current_user") if ctx.obj and "current_user" in ctx.obj else None

        if not current_user:
            # Default user for CLI usage (when no authentication system)
            current_user = Collaborator(
                id="cli-temp-manager",
                created_by_id="system",
                first_name="CLI",
                last_name="Manager",
                email="cli.manager@example.com",
                password="securepassword",
                phone_number="0000000000",
                role=Role.MANAGEMENT,
            )

        auth_context = AuthContext(current_user)
        use_case = SignContractUseCase(contract_repository, auth_context)

        use_case.execute(current_user.id, existing_contract.id)
        click.echo(f"✅ Contract with ID '{id}' has been signed successfully.")

    except Exception as e:
        click.echo(f"❌ An error occurred: {e}")
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
