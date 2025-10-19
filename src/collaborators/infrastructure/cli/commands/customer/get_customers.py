import click

from collaborators.application.customer.get_customers_use_case import GetCustomersUseCase
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_customer_repository import SqlalchemyCustomerRepository


@click.command("get-customers", help="Retrieve and display all customers")
@click.pass_context
@require_auth(Permissions.READ_CUSTOMERS)
def get_customers(ctx):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()
    auth_context = ctx.obj.get("auth_context")

    try:
        repository = SqlalchemyCustomerRepository(session)
        use_case = GetCustomersUseCase(auth_context, repository)
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
