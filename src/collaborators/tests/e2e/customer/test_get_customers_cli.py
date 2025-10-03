from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.customer import customer
from collaborators.infrastructure.repositories.sqlalchemy_customer_repository import SqlalchemyCustomerRepository


def test_collaborator_get_customers_cli(session, john_commercial, karim_customer, marie_customer):
    repo = SqlalchemyCustomerRepository(session)
    repo.create(karim_customer)
    repo.create(marie_customer)
    logged_user = john_commercial

    runner = CliRunner()
    result = runner.invoke(
        customer,
        ["get-customers"],
        obj={"session": session, "current_user": logged_user},
    )

    assert result.exit_code == 0
    assert "List of Customers:" in result.output
    assert "Karim" in result.output
    assert "Marie" in result.output
