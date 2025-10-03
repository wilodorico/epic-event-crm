import click

from collaborators.application.customer.update_customer_use_case import UpdateCustomerUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.infrastructure.cli.decorators import require_login
from collaborators.infrastructure.cli.inputs_validator import validate_email, validate_phone
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_customer_repository import SqlalchemyCustomerRepository


@click.command("update-customer")
@click.option("--id", prompt=True, type=str, help="ID of the customer to update")
@click.pass_context
@require_login
def update_customer(ctx, id):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()
    current_user = ctx.obj["current_user"]
    try:
        repository = SqlalchemyCustomerRepository(session)

        existing_customer = repository.find_by_id(id)
        if not existing_customer:
            click.echo(f"❌ Customer with ID '{id}' not found.")
            return

        click.echo(f"Updating customer: {existing_customer.first_name} {existing_customer.last_name}")
        click.echo("Press Enter to keep current value, or type new value:")
        click.echo()

        first_name = click.prompt("First name", default=existing_customer.first_name, show_default=True)
        last_name = click.prompt("Last name", default=existing_customer.last_name, show_default=True)
        email = click.prompt("Email", default=existing_customer.email, show_default=True)
        try:
            validate_email(None, None, email)
        except click.BadParameter as e:
            click.echo(f"❌ {e}")
            return

        phone_number = click.prompt("Phone number", default=existing_customer.phone_number, show_default=True)
        try:
            validate_phone(None, None, phone_number)
        except click.BadParameter as e:
            click.echo(f"❌ {e}")
            return

        company = click.prompt("Company", default=existing_customer.company, show_default=True)

        auth_context = AuthContext(current_user)
        use_case = UpdateCustomerUseCase(repository, auth_context)

        update_data = {}
        if first_name != existing_customer.first_name:
            update_data["first_name"] = first_name
        if last_name != existing_customer.last_name:
            update_data["last_name"] = last_name
        if email != existing_customer.email:
            update_data["email"] = email
        if phone_number != existing_customer.phone_number:
            update_data["phone_number"] = phone_number
        if company != existing_customer.company:
            update_data["company"] = company

        if not update_data:
            click.echo("No changes detected. Customer not updated.")
            return

        use_case.execute(current_user, existing_customer.id, update_data)
        click.echo("✅ Customer updated successfully.")

    except Exception as e:
        click.echo(f"❌ Error updating customer: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
