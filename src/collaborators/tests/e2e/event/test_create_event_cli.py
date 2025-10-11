import pytest
from click.testing import CliRunner


def event():
    pass  # Placeholder for the actual event command import


@pytest.mark.skip(reason="CLI test currently disabled")
def test_commercial_can_create_event_cli(session, john_commercial, karim_customer, karim_contract):
    logged_user = john_commercial

    user_input = (
        "General assembly\n"  # --event-name
        f"{karim_customer.id}\n"  # --customer-id
        f"{karim_contract.id}\n"  # --contract-id
        "2024-12-25 14:00\n"  # --event-date-start
        "2024-12-25 18:00\n"  # --event-date-end
        "Banquet hall\n"  # --location
        "100\n"  # --attendees
        "General assembly for all employees\n"  # --notes
    )

    runner = CliRunner()

    result = runner.invoke(event, ["create"], input=user_input, obj={"session": session, "current_user": logged_user})

    assert result.exit_code == 0
    assert "✅ Event Christmas Party created successfully" in result.output
