from datetime import datetime

import click

from collaborators.application.event.create_event_use_case import CreateEventUseCase
from collaborators.domain.collaborator.permissions import Permissions
from collaborators.infrastructure.cli.decorators import require_auth
from collaborators.infrastructure.database.db import SessionLocal
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository
from collaborators.infrastructure.repositories.sqlalchemy_event_repository import SqlalchemyEventRepository
from commons.uuid_generator import UuidGenerator


@click.command("create")
@click.pass_context
@require_auth(Permissions.CREATE_EVENT)
@click.option("--contract-id", prompt=True, type=str)
@click.option("--title", prompt=True, type=str)
@click.option("--date-start", prompt=True, type=str)
@click.option("--date-end", prompt=True, type=str)
@click.option("--location", prompt=True, type=str)
@click.option("--attendees", prompt=True, type=int)
@click.option("--notes", prompt=True, type=str)
def create_event(ctx, contract_id, title, date_start, date_end, location, attendees, notes):
    session = ctx.obj.get("session") if ctx.obj and "session" in ctx.obj else SessionLocal()
    current_user = ctx.obj.get("current_user")
    auth_context = ctx.obj.get("auth_context")

    try:
        repository = SqlalchemyEventRepository(session)
        contract_repository = SqlalchemyContractRepository(session)
        uuid_generator = UuidGenerator()

        # Convert string dates to datetime objects
        date_start_dt = datetime.strptime(date_start, "%Y-%m-%d %H:%M")
        date_end_dt = datetime.strptime(date_end, "%Y-%m-%d %H:%M")

        use_case = CreateEventUseCase(repository, contract_repository, uuid_generator, auth_context)
        event = use_case.execute(
            creator=current_user,
            contract_id=contract_id,
            title=title,
            date_start=date_start_dt,
            date_end=date_end_dt,
            location=location,
            attendees=attendees,
            notes=notes,
        )

        click.echo(f"✅ Event {event.title} created successfully with ID: {event.id}")
    except Exception as e:
        click.echo(f"❌ Error creating event: {str(e)}")
        raise
    finally:
        if not (ctx.obj and "session" in ctx.obj):
            session.close()
