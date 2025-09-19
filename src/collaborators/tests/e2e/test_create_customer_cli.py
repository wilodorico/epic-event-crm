from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.customer import customer
from collaborators.infrastructure.repositories.sqlalchemy_customer_repository import SqlalchemyCustomerRepository


def test_create_customer_success_cli(session):
    user_input = (
        "Karim\n"  # --first-name
        "Smith\n"  # --last-name
        "karim.smith@example.com\n"  # --email
        "0601020304\n"  # --phone-number
        "Techland\n"  # --company-name
    )

    runner = CliRunner()
    result = runner.invoke(customer, ["create-customer"], input=user_input, obj={"session": session})

    assert result.exit_code == 0
    assert "✅ Customer Karim Smith created successfully" in result.output

    repo = SqlalchemyCustomerRepository(session)
    created_customer = repo.find_by_email("karim.smith@example.com")

    assert created_customer is not None
    assert created_customer.first_name == "Karim"
    assert created_customer.last_name == "Smith"
    assert created_customer.email == "karim.smith@example.com"
    assert created_customer.phone_number == "0601020304"
    assert created_customer.company == "Techland"
    assert created_customer.commercial_contact_id == "cli-temp-commercial"
    assert created_customer.id is not None  # UUID should be generated
