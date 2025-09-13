from click.testing import CliRunner

from collaborators.infrastructure.cli import create_collaborator


def test_create_collaborator_wrong_email_cli():
    runner = CliRunner()
    result = runner.invoke(create_collaborator, input="wilfried\npeter\nwrong-email\n0601020304\nMANAGEMENT\n")
    assert result.exit_code == 1
    assert "Invalid email address" in result.output
