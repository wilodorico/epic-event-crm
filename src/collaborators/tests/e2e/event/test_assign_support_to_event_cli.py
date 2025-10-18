from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.event import event
from collaborators.infrastructure.repositories.sqlalchemy_event_repository import SqlalchemyEventRepository


def test_manager_can_assign_support_to_event_cli(session, manager_alice, bob_support, karim_event):
    logged_user = manager_alice
    repo = SqlalchemyEventRepository(session)
    repo.create(karim_event)
    user_input = (
        f"{karim_event.id}\n"  # Select event ID
        f"{bob_support.id}\n"  # Support collaborator ID to assign
    )

    runner = CliRunner()
    result = runner.invoke(
        event,
        ["assign-support"],
        input=user_input,
        obj={"session": session, "current_user": logged_user},
    )

    assert result.exit_code == 0
    assert f"✅ Support assigned to '{karim_event.title}' successfully." in result.output

    updated_event = repo.find_by_id(karim_event.id)
    assert updated_event is not None
    assert updated_event.contact_support_id == bob_support.id
