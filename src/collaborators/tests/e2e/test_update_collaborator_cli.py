import pytest
from click.testing import CliRunner

from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.cli.commands.collaborator import collaborator
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)


@pytest.fixture
def collaborator_to_update():
    return Collaborator(
        id="id-collaborator-to-update",
        created_by_id="system",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="oldpassword",
        phone_number="1234567890",
        role=Role.COMMERCIAL,
    )


def test_update_collaborator_success_cli(session, collaborator_to_update):
    """Test successful update of a collaborator through CLI."""
    repo = SqlalchemyCollaboratorRepository(session)
    repo.create(collaborator_to_update)

    # CLI input for updating the collaborator
    # Expected interface: update-collaborator --id <id> with prompts for fields to update
    user_input = (
        "Johnny\n"  # --first-name (new value)
        "Smith\n"  # --last-name (new value)
        "johnny.smith@example.com\n"  # --email (new value)
        "0987654321\n"  # --phone-number (new value)
        f"{Role.SUPPORT.value}\n"  # --role (new value)
    )

    runner = CliRunner()
    result = runner.invoke(
        collaborator,
        ["update-collaborator", "--id", "id-collaborator-to-update"],
        input=user_input,
        obj={"session": session},
    )

    assert result.exit_code == 0
    assert "✅ Collaborator Johnny Smith updated successfully!" in result.output

    updated_collaborator = repo.find_by_id("id-collaborator-to-update")

    assert updated_collaborator is not None
    assert updated_collaborator.first_name == "Johnny"
    assert updated_collaborator.last_name == "Smith"
    assert updated_collaborator.email == "johnny.smith@example.com"
    assert updated_collaborator.phone_number == "0987654321"
    assert updated_collaborator.role == Role.SUPPORT
    assert updated_collaborator.id == "id-collaborator-to-update"  # ID should not change
    assert updated_collaborator.updated_at is not None  # Should be updated


def test_update_collaborator_non_existent_id_cli(session):
    """Test updating a collaborator with a non-existent ID through CLI."""
    runner = CliRunner()
    result = runner.invoke(
        collaborator,
        ["update-collaborator", "--id", "non-existent-id"],
        input="\n\n\n\n\n",  # Just pressing Enter for all prompts
        obj={"session": session},
    )

    assert result.exit_code == 0
    assert "❌ Collaborator with ID 'non-existent-id' not found." in result.output


def test_update_collaborator_invalid_email_cli(session):
    """Test updating a collaborator with an invalid email through CLI."""
    repo = SqlalchemyCollaboratorRepository(session)
    existing_collaborator = Collaborator(
        id="id-collaborator-to-update",
        created_by_id="system",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="oldpassword",
        phone_number="1234567890",
        role=Role.COMMERCIAL,
    )
    repo.create(existing_collaborator)
    user_input = (
        "\n"  # --first-name (keep current)
        "\n"  # --last-name (keep current)
        "wrong-email\n"  # --email (invalid)
        "\n"  # --phone-number (keep current)
        "\n"  # --role (keep current)
    )
    runner = CliRunner()
    result = runner.invoke(
        collaborator,
        ["update-collaborator", "--id", "id-collaborator-to-update"],
        input=user_input,
        obj={"session": session},
    )
    assert result.exit_code == 0
    assert "Invalid email address" in result.output


def test_update_collaborator_invalid_phone_cli(session, collaborator_to_update):
    """Test updating a collaborator with an invalid phone number through CLI."""
    repo = SqlalchemyCollaboratorRepository(session)
    repo.create(collaborator_to_update)

    user_input = (
        "\n"  # --first-name (keep current)
        "\n"  # --last-name (keep current)
        "\n"  # --email (keep current)
        "12345\n"  # --phone-number (invalid - too short)
        "\n"  # --role (keep current)
    )

    runner = CliRunner()
    result = runner.invoke(
        collaborator,
        ["update-collaborator", "--id", "id-collaborator-to-update"],
        input=user_input,
        obj={"session": session},
    )

    assert result.exit_code == 0
    assert "Invalid phone number (10 digits expected)" in result.output
