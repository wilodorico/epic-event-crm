import click

from collaborators.application.contract.create_contract_use_case import CreateContractUseCase
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth
from collaborators.infrastructure.cli.inputs_validator import validate_positive_decimal
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository
from collaborators.infrastructure.repositories.sqlalchemy_customer_repository import SqlalchemyCustomerRepository
from commons.uuid_generator import UuidGenerator


@click.command("create-contract", help="Create a new contract")
@click.pass_context
@require_auth(Permissions.CREATE_CONTRACT)
@click.option("--customer-id", prompt="Customer ID", help="ID of the customer")
@click.option(
    "--total-amount", prompt="Total Amount", callback=validate_positive_decimal, help="Total amount of the contract"
)
@click.option(
    "--remaining-amount",
    prompt="Remaining Amount",
    callback=validate_positive_decimal,
    help="Remaining amount of the contract",
)
def create_contract(ctx, customer_id, total_amount, remaining_amount):
    """Create a new contract for a customer"""
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()
    current_user = ctx.obj.get("current_user")
    auth_context = ctx.obj.get("auth_context")

    try:
        customer_repository = SqlalchemyCustomerRepository(session)
        contract_repository = SqlalchemyContractRepository(session)
        id_generator = UuidGenerator()

        use_case = CreateContractUseCase(customer_repository, contract_repository, id_generator, auth_context)

        contract = use_case.execute(
            creator=current_user,
            customer_id=customer_id,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
        )

        click.echo(f"✅ Contract {contract.id} created successfully")
    except Exception as e:
        click.echo(f"❌ Error creating contract: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
