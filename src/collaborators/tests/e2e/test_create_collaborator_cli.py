from click.testing import CliRunner

from collaborators.domain.collaborator.collaborator import Role
from collaborators.infrastructure.cli.commands.collaborator import collaborator
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)


def test_create_collaborator_wrong_email_cli(session):
    user_input = (
        "wilfried\n"  # --first-name
        "peter\n"  # --last-name
        "wrong-email\n"  # --email (should fail validation)
        "secretpass\n"  # --password
        "secretpass\n"  # confirm password
        "0601020304\n"  # --phone-number
        f"{Role.MANAGEMENT.value}\n"  # --role
    )
    runner = CliRunner()
    result = runner.invoke(collaborator, ["create-collaborator"], input=user_input, obj={"session": session})
    assert result.exit_code == 1
    assert "Invalid email address" in result.output

    repo = SqlalchemyCollaboratorRepository(session)
    assert repo.find_by_email("wrong-email") is None
