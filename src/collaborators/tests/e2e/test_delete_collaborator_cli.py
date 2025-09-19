from click.testing import CliRunner

from collaborators.domain.collaborator.collaborator import Collaborator, Role
from collaborators.infrastructure.cli.commands.collaborator import collaborator
from collaborators.infrastructure.repositories.sqlalchemy_collaborator_repository import (
    SqlalchemyCollaboratorRepository,
)


def test_delete_collaborator_success_cli(session):
    """Test successful deletion of a collaborator through CLI."""
    repo = SqlalchemyCollaboratorRepository(session)
    collaborator_to_delete = Collaborator(
        id="id-collaborator-to-delete",
        created_by_id="system",
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        password="securepassword",
        phone_number="1234567890",
        role=Role.COMMERCIAL,
    )
    repo.create(collaborator_to_delete)

    runner = CliRunner()
    result = runner.invoke(
        collaborator,
        ["delete-collaborator", "--id", "id-collaborator-to-delete"],
        obj={"session": session},
    )

    assert result.exit_code == 0
    assert "✅ Collaborator Jane Doe deleted successfully!" in result.output

    deleted_collaborator = repo.find_by_id("id-collaborator-to-delete")
    assert deleted_collaborator is None
