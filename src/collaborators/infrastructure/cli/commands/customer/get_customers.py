import click

from collaborators.application.customer.get_customers_use_case import GetCustomersUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.infrastructure.cli.decorators import require_login
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_customer_repository import SqlalchemyCustomerRepository


@click.command("get-customers", help="Retrieve and display all customers")
@click.pass_context
@require_login
def get_customers(ctx):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()
    current_user = ctx.obj["current_user"]

    try:
        repository = SqlalchemyCustomerRepository(session)
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
