import click

from collaborators.application.customer.create_customer_use_case import CreateCustomerUseCase
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth
from collaborators.infrastructure.cli.inputs_validator import validate_email, validate_phone
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_customer_repository import SqlalchemyCustomerRepository
from commons.uuid_generator import UuidGenerator


@click.command("create-customer")
@click.pass_context
@require_auth(Permissions.CREATE_CUSTOMER)
@click.option("--first-name", prompt=True, type=str)
@click.option("--last-name", prompt=True, type=str)
@click.option("--email", prompt=True, callback=validate_email)
@click.option("--phone-number", prompt=True, callback=validate_phone)
@click.option("--company", prompt=True, type=str)
def create_customer(ctx, first_name, last_name, email, phone_number, company):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()
    current_user = ctx.obj.get("current_user")
    auth_context = ctx.obj.get("auth_context")

    try:
        repository = SqlalchemyCustomerRepository(session)
        id_generator = UuidGenerator()

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
