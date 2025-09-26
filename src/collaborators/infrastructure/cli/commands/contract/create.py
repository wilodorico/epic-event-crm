import click

from collaborators.application.contract.create_contract_use_case import CreateContractUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository
from collaborators.infrastructure.repositories.sqlalchemy_customer_repository import SqlalchemyCustomerRepository
from commons.uuid_generator import UuidGenerator


@click.command("create-contract", help="Create a new contract")
@click.option("--customer-id", prompt="Customer ID", type=str, help="ID of the customer")
@click.option("--total-amount", prompt="Total Amount", type=float, help="Total amount of the contract")
@click.option("--remaining-amount", prompt="Remaining Amount", type=float, help="Remaining amount of the contract")
@click.pass_context
def create_contract(ctx, customer_id, total_amount, remaining_amount):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else None

    try:
        customer_repository = SqlalchemyCustomerRepository(session)
        contract_repository = SqlalchemyContractRepository(session)
        id_generator = UuidGenerator()

        # Get user from context (for tests) or use default
        current_user = ctx.obj.get("current_user") if ctx.obj and "current_user" in ctx.obj else None

        if not current_user:
            # Default user for CLI usage (when no authentication system)
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
