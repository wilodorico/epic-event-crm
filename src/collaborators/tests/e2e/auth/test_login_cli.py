import os

import pytest
from click.testing import CliRunner

from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.cli.commands.auth import auth
from collaborators.infrastructure.cli.commands.customer import customer
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)
from collaborators.infrastructure.security.jwt_service import JWTService
from collaborators.tests.fakes.fake_password_hasher import FakePasswordHasher

SESSION_FILE = ".crm_session"


@pytest.fixture(autouse=True)
def cleanup_session_file():
    """Removes the session before/after each test"""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    yield
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)


@pytest.fixture
def test_user(session):
    """Creates a test user in the database"""
    repo = SqlalchemyCollaboratorRepository(session)
    password_hasher = FakePasswordHasher()

    user = Collaborator(
        id="test-user-id",
        created_by_id="system",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password=password_hasher.hash("password123"),
        phone_number="0123456789",
        role=Role.COMMERCIAL,
    )
    repo.create(user)
    return user


def test_login_with_valid_credentials(session, test_user):
    """Test login with valid credentials"""
    runner = CliRunner()
    user_input = f"{test_user.email}\npassword123\n"

    result = runner.invoke(auth, ["login"], input=user_input, obj={"session": session, "test_env": True})

    assert result.exit_code == 0
    assert f"✅ Logged in as {test_user.first_name} {test_user.last_name}" in result.output
    assert os.path.exists(SESSION_FILE)


def test_login_with_invalid_email(session, test_user):
    """Test login with an invalid email"""
    runner = CliRunner()
    user_input = "wrong.email@example.com\npassword123\n"

    result = runner.invoke(auth, ["login"], input=user_input, obj={"session": session, "test_env": True})

    assert "❌ Invalid email or password" in result.output
    assert not os.path.exists(SESSION_FILE)


def test_login_with_invalid_password(session, test_user):
    """Test login with an invalid password"""
    runner = CliRunner()
    user_input = f"{test_user.email}\nwrongpassword\n"

    result = runner.invoke(auth, ["login"], input=user_input, obj={"session": session, "test_env": True})

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

    result = runner.invoke(auth, ["login"], input=user_input, obj={"session": session, "test_env": True})

    assert result.exit_code == 0
    assert os.path.exists(SESSION_FILE)

    with open(SESSION_FILE, "r") as f:
        session_data = json.load(f)

    assert "token" in session_data

    jwt_service = JWTService()
    decoded_token = jwt_service.decode(session_data["token"])

    assert decoded_token["id"] == test_user.id
    assert decoded_token["email"] == test_user.email
    assert decoded_token["role"] == test_user.role.value
    assert f"✅ Logged in as {test_user.first_name} {test_user.last_name}" in result.output


def test_session_file_content(session, test_user):
    """Test that the session file contains the correct information"""
    import json

    runner = CliRunner()
    user_input = f"{test_user.email}\npassword123\n"

    result = runner.invoke(auth, ["login"], input=user_input, obj={"session": session, "test_env": True})

    assert result.exit_code == 0
    assert os.path.exists(SESSION_FILE)

    # Check the content of the session file
    with open(SESSION_FILE, "r") as f:
        session_data = json.load(f)

    assert "token" in session_data

    jwt_service = JWTService()
    decoded_token = jwt_service.decode(session_data["token"])

    assert decoded_token["id"] == test_user.id
    assert decoded_token["email"] == test_user.email
    assert decoded_token["role"] == test_user.role.value


def test_multiple_logins_overwrite_session(session, test_user):
    """Test that multiple consecutive logins overwrite the previous session"""
    runner = CliRunner()
    user_input = f"{test_user.email}\npassword123\n"

    # First login
    result1 = runner.invoke(auth, ["login"], input=user_input, obj={"session": session, "test_env": True})
    assert result1.exit_code == 0

    # Second login
    result2 = runner.invoke(auth, ["login"], input=user_input, obj={"session": session, "test_env": True})
    assert result2.exit_code == 0

    # The session file must still exist and be valid
    assert os.path.exists(SESSION_FILE)
