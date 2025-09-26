import click

from collaborators.application.customer.get_customers_use_case import GetCustomersUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_customer_repository import SqlalchemyCustomerRepository


@click.command("get-customers", help="Retrieve and display all customers")
@click.pass_context
def get_customers(ctx):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()

    try:
        repository = SqlalchemyCustomerRepository(session)

        # Get user from context (for tests) or use default
        current_user = ctx.obj.get("current_user") if ctx.obj and "current_user" in ctx.obj else None

        if not current_user:
            # Default user for CLI usage (when no authentication system)
            current_user = Collaborator(
                id="cli-temp-commercial",
                created_by_id="system",
                first_name="CLI",
                last_name="Commercial",
                email="cli.temp@test.com",
                password="securepassword",
                phone_number="0000000000",
                role=Role.COMMERCIAL,
            )

        auth_context = AuthContext(current_user)
        use_case = GetCustomersUseCase(repository, auth_context)

        customers = use_case.execute()

        if not customers:
            click.echo("No customers found.")
            return

        click.echo("List of Customers:")

        for customer in customers:
            click.echo(f"- {customer.first_name} {customer.last_name} (ID: {customer.id})")

    except Exception as e:
        click.echo(f"❌ Error retrieving customers: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
