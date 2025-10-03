import click

from collaborators.application.customer.create_customer_use_case import CreateCustomerUseCase
from collaborators.application.services.auth_context import AuthContext
from collaborators.infrastructure.cli.decorators import require_login
from collaborators.infrastructure.cli.inputs_validator import validate_email, validate_phone
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_customer_repository import SqlalchemyCustomerRepository
from commons.uuid_generator import UuidGenerator


@click.command("create-customer")
@click.option("--first-name", prompt=True, type=str)
@click.option("--last-name", prompt=True, type=str)
@click.option("--email", prompt=True, callback=validate_email)
@click.option("--phone-number", prompt=True, callback=validate_phone)
@click.option("--company", prompt=True, type=str)
@click.pass_context
@require_login
def create_customer(ctx, first_name, last_name, email, phone_number, company):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()
    current_user = ctx.obj.get("current_user")

    try:
        repository = SqlalchemyCustomerRepository(session)
        id_generator = UuidGenerator()

        auth_context = AuthContext(current_user)
        use_case = CreateCustomerUseCase(repository, id_generator, auth_context)
        customer = use_case.execute(
            creator=current_user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            company=company,
        )
        click.echo(
            f"✅ Customer {customer.first_name} {customer.last_name} created successfully with ID: {customer.id}"
        )
    except Exception as e:
        click.echo(f"❌ Error creating customer: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
