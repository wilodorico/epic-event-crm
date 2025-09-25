import pytest
from click.testing import CliRunner

from collaborators.domain.customer.customer import Customer
from collaborators.infrastructure.cli.commands.customer import customer
from collaborators.infrastructure.repositories.sqlalchemy_customer_repository import SqlalchemyCustomerRepository


@pytest.fixture
def john_customer_to_update(john_commercial):
    return Customer(
        id="id-john-customer-to-update",
        first_name="Alice",
        last_name="Wonderland",
        email="alice.wonderland@test.com",
        phone_number="1234567890",
        company="Wonderland Inc.",
        commercial_contact_id=john_commercial.id,
    )


@pytest.fixture
def amel_customer_to_update(amel_commercial):
    return Customer(
        id="id-amel-customer-to-update",
        first_name="Bob",
        last_name="Smith",
        email="bob.smith@test.com",
        phone_number="0987654321",
        company="Smith Corp",
        commercial_contact_id=amel_commercial.id,
    )


def test_update_customer_success_cli(session, john_customer_to_update, john_commercial):
    repo = SqlalchemyCustomerRepository(session)
    repo.create(john_customer_to_update)

    user_input = (
        "Alicia\n"  # --first-name (new value)
        "Smith\n"  # --last-name (new value)
        "alicia.smith@wonderland.com\n"  # --email (new value)
        "0987654321\n"  # --phone-number (new value)
        "Wonderland Tech\n"  # --company (new value)
    )

    runner = CliRunner()
    result = runner.invoke(
        customer,
        ["update-customer", "--id", "id-john-customer-to-update"],
        input=user_input,
        obj={"session": session},
    )

    assert result.exit_code == 0
    assert "Customer updated successfully." in result.output

    updated_customer = repo.find_by_id("id-john-customer-to-update")
    assert updated_customer is not None
    assert updated_customer.first_name == "Alicia"
    assert updated_customer.last_name == "Smith"
    assert updated_customer.email == "alicia.smith@wonderland.com"
    assert updated_customer.phone_number == "0987654321"
    assert updated_customer.company == "Wonderland Tech"
    assert updated_customer.commercial_contact_id == john_commercial.id


def test_update_customer_non_existent_id_cli(session):
    runner = CliRunner()
    result = runner.invoke(
        customer,
        ["update-customer", "--id", "non-existent-id"],
        input="",
        obj={"session": session},
    )

    assert result.exit_code == 0
    assert "❌ Customer with ID 'non-existent-id' not found." in result.output


def test_cant_update_customer_if_not_my_customer_cli(session, amel_customer_to_update):
    """Test that updating a customer not assigned to the commercial fails."""
    repo = SqlalchemyCustomerRepository(session)
    repo.create(amel_customer_to_update)

    user_input = (
        "Alicia\n"  # --first-name (new value)
        "Smith\n"  # --last-name (new value)
        "alicia.smith@wonderland.com\n"  # --email (new value)
        "0987654321\n"  # --phone-number (new value)
        "Wonderland Tech\n"  # --company (new value)
    )

    runner = CliRunner()
    result = runner.invoke(
        customer,
        ["update-customer", "--id", "id-amel-customer-to-update"],
        input=user_input,
        obj={"session": session},
    )

    assert result.exit_code == 1
    assert "You can only update your own customers" in result.output
