import os

import pytest
from click.testing import CliRunner

from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.cli.commands.auth import auth
from collaborators.infrastructure.cli.commands.customer import customer
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)

SESSION_FILE = ".crm_session"


@pytest.fixture(autouse=True)
def cleanup_session_file():
    """Supprime la session avant/après chaque test"""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    yield
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)


@pytest.fixture
def test_user(session):
    """Creates a test user in the database"""
    repo = SqlalchemyCollaboratorRepository(session)
    user = Collaborator(
        id="test-user-id",
        created_by_id="system",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="password123",  # Note: In production, use a hash
        phone_number="0123456789",
        role=Role.COMMERCIAL,
    )
    repo.create(user)
    return user


def test_login_with_valid_credentials(session, test_user):
    """Test login with valid credentials"""
    runner = CliRunner()
    user_input = f"{test_user.email}\npassword123\n"

    result = runner.invoke(auth, ["login"], input=user_input, obj={"session": session})

    assert result.exit_code == 0
    assert f"✅ Logged in as {test_user.first_name} {test_user.last_name}" in result.output
    assert os.path.exists(SESSION_FILE)


def test_login_with_invalid_email(session, test_user):
    """Test login with an invalid email"""
    runner = CliRunner()
    user_input = "wrong.email@example.com\npassword123\n"

    result = runner.invoke(auth, ["login"], input=user_input, obj={"session": session})

    assert "❌ Invalid email or password" in result.output
    assert not os.path.exists(SESSION_FILE)


def test_login_with_invalid_password(session, test_user):
    """Test login with an invalid password"""
    runner = CliRunner()
    user_input = f"{test_user.email}\nwrongpassword\n"

    result = runner.invoke(auth, ["login"], input=user_input, obj={"session": session})

    assert "❌ Invalid email or password" in result.output
    assert not os.path.exists(SESSION_FILE)


def test_access_protected_command_without_login(session):
    """Test that a protected command is blocked without login"""
    runner = CliRunner()

    result = runner.invoke(customer, ["get-customers"], obj={"session": session})

    assert "❌ You must login first" in result.output


def test_login_creates_valid_session_file(session, test_user):
    """Test that login creates a session file with correct data"""
    import json

    runner = CliRunner()
    user_input = f"{test_user.email}\npassword123\n"

    result = runner.invoke(auth, ["login"], input=user_input, obj={"session": session})

    assert result.exit_code == 0
    assert os.path.exists(SESSION_FILE)

    with open(SESSION_FILE, "r") as f:
        session_data = json.load(f)

    assert session_data["id"] == test_user.id
    assert session_data["email"] == test_user.email
    assert session_data["role"] == test_user.role.value
    assert f"✅ Logged in as {test_user.first_name} {test_user.last_name}" in result.output


def test_session_file_content(session, test_user):
    """Test that the session file contains the correct information"""
    import json

    runner = CliRunner()
    user_input = f"{test_user.email}\npassword123\n"

    result = runner.invoke(auth, ["login"], input=user_input, obj={"session": session})

    assert result.exit_code == 0
    assert os.path.exists(SESSION_FILE)

    # Check the content of the session file
    with open(SESSION_FILE, "r") as f:
        session_data = json.load(f)

    assert session_data["id"] == test_user.id
    assert session_data["email"] == test_user.email
    assert session_data["role"] == test_user.role.value


def test_multiple_logins_overwrite_session(session, test_user):
    """Test that multiple consecutive logins overwrite the previous session"""
    runner = CliRunner()
    user_input = f"{test_user.email}\npassword123\n"

    # First login
    result1 = runner.invoke(auth, ["login"], input=user_input, obj={"session": session})
    assert result1.exit_code == 0

    # Second login
    result2 = runner.invoke(auth, ["login"], input=user_input, obj={"session": session})
    assert result2.exit_code == 0

    # The session file must still exist and be valid
    assert os.path.exists(SESSION_FILE)


def test_login_prompt_messages(session, test_user):
    """Test that prompt messages are displayed correctly"""
    runner = CliRunner()
    user_input = f"{test_user.email}\npassword123\n"

    result = runner.invoke(auth, ["login"], input=user_input, obj={"session": session})

    assert "Email:" in result.output
    assert "Password:" in result.output
