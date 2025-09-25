from click.testing import CliRunner

from collaborators.domain.customer.customer import Customer
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


def test_create_customer_wrong_email_cli(session):
    user_input = (
        "Karim\n"  # --first-name
        "Smith\n"  # --last-name
        "karim.smith@.com\n"  # --email (wrong)
        "0601020304\n"  # --phone-number
        "Techland\n"  # --company-name
    )

    runner = CliRunner()
    result = runner.invoke(customer, ["create-customer"], input=user_input, obj={"session": session})

    assert result.exit_code != 0
    assert "Invalid email address" in result.output

    repo = SqlalchemyCustomerRepository(session)
    created_customer = repo.find_by_email("karim.smith@.com")

    assert created_customer is None


def test_cant_create_customer_with_existing_email_cli(session, john_commercial):
    """Test that creating a customer with an existing email fails."""
    repo = SqlalchemyCustomerRepository(session)
    existing_customer = Customer(
        id="existing-id",
        first_name="Existing",
        last_name="Customer",
        email="existing.customer@example.com",
        phone_number="0601020304",
        company="Techland",
        commercial_contact_id=john_commercial.id,
    )
    repo.create(existing_customer)

    user_input = (
        "Karim\n"  # --first-name
        "Smith\n"  # --last-name
        "existing.customer@example.com\n"  # --email
        "0601020304\n"  # --phone-number
        "Techland\n"  # --company-name
    )

    runner = CliRunner()
    result = runner.invoke(customer, ["create-customer"], input=user_input, obj={"session": session})

    assert result.exit_code == 1
    assert "Email already exists" in result.output

    repo = SqlalchemyCustomerRepository(session)
    customer_count = repo.count()

    assert customer_count == 1  # Still only the existing customer
