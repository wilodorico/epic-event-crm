from click.testing import CliRunner

from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.cli.commands.collaborator import collaborator
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)


def test_create_collaborator_success_cli(session, manager_alice):
    """Test successful creation of a collaborator through CLI."""
    user_input = (
        "Wilfried\n"  # --first-name
        "Peter\n"  # --last-name
        "wilfried.peter@example.com\n"  # --email
        "secretpass123\n"  # --password
        "secretpass123\n"  # confirm password
        "0601020304\n"  # --phone-number
        f"{Role.COMMERCIAL.value}\n"  # --role
    )
    logged_user = manager_alice

    runner = CliRunner()
    result = runner.invoke(
        collaborator, ["create-collaborator"], input=user_input, obj={"session": session, "current_user": logged_user}
    )

    # Verify the command succeeded
    assert result.exit_code == 0
    assert "✅ Collaborator Wilfried Peter created!" in result.output

    # Verify the collaborator was actually created in the database
    repo = SqlalchemyCollaboratorRepository(session)
    created_collaborator = repo.find_by_email("wilfried.peter@example.com")

    assert created_collaborator is not None
    assert created_collaborator.first_name == "Wilfried"
    assert created_collaborator.last_name == "Peter"
    assert created_collaborator.email == "wilfried.peter@example.com"
    assert created_collaborator.phone_number == "0601020304"
    assert created_collaborator.role == Role.COMMERCIAL
    assert created_collaborator.id is not None  # UUID should be generated
    assert created_collaborator.created_by_id == manager_alice.id


def test_create_collaborator_wrong_email_cli(session, manager_alice):
    user_input = (
        "wilfried\n"  # --first-name
        "peter\n"  # --last-name
        "wrong-email\n"  # --email (should fail validation)
        "secretpass\n"  # --password
        "secretpass\n"  # confirm password
        "0601020304\n"  # --phone-number
        f"{Role.MANAGEMENT.value}\n"  # --role
    )
    logged_user = manager_alice
    runner = CliRunner()
    result = runner.invoke(
        collaborator, ["create-collaborator"], input=user_input, obj={"session": session, "current_user": logged_user}
    )
    assert result.exit_code == 1
    assert "Invalid email address" in result.output

    repo = SqlalchemyCollaboratorRepository(session)
    assert repo.find_by_email("wrong-email") is None


def test_create_collaborator_wrong_phone_cli(session, manager_alice):
    """Test creation fails with invalid phone number."""
    user_input = (
        "John\n"  # --first-name
        "Doe\n"  # --last-name
        "john.doe@example.com\n"  # --email
        "password123\n"  # --password
        "password123\n"  # confirm password
        "123456789\n"  # --phone-number (invalid - only 9 digits)
        f"{Role.SUPPORT.value}\n"  # --role
    )
    logged_user = manager_alice
    runner = CliRunner()
    result = runner.invoke(
        collaborator, ["create-collaborator"], input=user_input, obj={"session": session, "current_user": logged_user}
    )

    assert result.exit_code == 1
    assert "Invalid phone number (10 digits expected)" in result.output

    repo = SqlalchemyCollaboratorRepository(session)
    assert repo.find_by_email("john.doe@example.com") is None


def test_create_collaborator_duplicate_email_cli(session, manager_alice):
    """Test creation fails when email already exists."""
    repo = SqlalchemyCollaboratorRepository(session)

    existing_collaborator = Collaborator(
        id="existing-id",
        created_by_id="system",
        first_name="Existing",
        last_name="User",
        email="duplicate@example.com",
        password="password",
        phone_number="1234567890",
        role=Role.MANAGEMENT,
    )
    repo.create(existing_collaborator)

    # Now try to create another with the same email
    user_input = (
        "Another\n"  # --first-name
        "User\n"  # --last-name
        "duplicate@example.com\n"  # --email (already exists)
        "password123\n"  # --password
        "password123\n"  # confirm password
        "0987654321\n"  # --phone-number
        f"{Role.COMMERCIAL.value}\n"  # --role
    )
    logged_user = manager_alice
    runner = CliRunner()
    result = runner.invoke(
        collaborator, ["create-collaborator"], input=user_input, obj={"session": session, "current_user": logged_user}
    )

    assert result.exit_code == 1
    assert "❌ Error creating collaborator:" in result.output
    assert "Email already exists" in result.output


def test_create_collaborator_without_permission_cli(session, jane_commercial):
    """Test that a commercial user cannot create a collaborator."""
    # Jane is a commercial user and should not have CREATE_COLLABORATOR permission
    logged_user = jane_commercial

    runner = CliRunner()
    result = runner.invoke(
        collaborator,
        ["create-collaborator"],
        input="",  # No input - should be rejected before prompts
        obj={"session": session, "current_user": logged_user},
    )

    # The user should be rejected immediately without prompts
    assert result.exit_code == 1
    assert "does not have permission" in result.output
    assert jane_commercial.email in result.output
    assert jane_commercial.role.value in result.output
    # Check that no prompt was displayed
    assert "First name" not in result.output
