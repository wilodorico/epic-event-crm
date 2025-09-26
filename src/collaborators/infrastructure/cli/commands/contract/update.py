import click

from collaborators.application.contract.update_contract_use_case import UpdateContractUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.cli.inputs_validator import validate_positive_decimal
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository


@click.command("update-contract", help="Update an existing contract")
@click.option("--id", prompt="Contract ID", type=str, help="ID of the contract to update")
@click.pass_context
def update_contract(ctx, id):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()

    try:
        contract_repository = SqlalchemyContractRepository(session)
        existing_contract = contract_repository.find_by_id(id)
        if not existing_contract:
            click.echo(f"❌ Contract with ID '{id}' not found.")
            return

        click.echo(f"Updating contract: {existing_contract.id}")
        click.echo("Press Enter to keep current value, or type new value:")
        click.echo()

        new_total_amount = click.prompt(
            f"Total Amount [{existing_contract.total_amount}]", default=existing_contract.total_amount
        )
        new_remaining_amount = click.prompt(
            f"Remaining Amount [{existing_contract.remaining_amount}]", default=existing_contract.remaining_amount
        )

        try:
            validate_positive_decimal(None, None, new_total_amount)
            validate_positive_decimal(None, None, new_remaining_amount)
        except click.BadParameter as e:
            click.echo(f"❌ {e}")
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
        use_case = UpdateContractUseCase(contract_repository, auth_context)

        update_data = {}
        if new_total_amount != existing_contract.total_amount:
            update_data["total_amount"] = new_total_amount
        if new_remaining_amount != existing_contract.remaining_amount:
            update_data["remaining_amount"] = new_remaining_amount
        if not update_data:
            click.echo("No changes detected. Contract not updated.")
            return

        updated_contract = use_case.execute(updater=current_user, contract_id=id, data=update_data)
        click.echo(f"✅ Contract {updated_contract.id} updated successfully")
    except Exception as e:
        click.echo(f"❌ Error updating contract: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
