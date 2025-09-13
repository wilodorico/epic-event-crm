import click

from collaborators.infrastructure.database.db import init_db


@click.command("init-db")
def init_db_command():
    """Initialize the database."""
    init_db()
    click.echo("✅ Database initialized!")
