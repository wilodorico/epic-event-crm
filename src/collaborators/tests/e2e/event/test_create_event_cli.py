from datetime import datetime, time, timedelta

from click.testing import CliRunner

from collaborators.infrastructure.cli.commands.event import event
from collaborators.infrastructure.repositories.sqlalchemy_contract_repository import SqlalchemyContractRepository


def generate_future_event_dates(days_ahead: int = 1, start_hour: int = 14, duration_hours: int = 4) -> tuple[str, str]:
    """
    Generate future event dates for testing purposes.

    Args:
        days_ahead: Number of days in the future for the event (default: 1)
        start_hour: Hour of the day when the event starts (default: 14 for 2 PM)
        duration_hours: Duration of the event in hours (default: 4)

    Returns:
        A tuple containing (start_date_str, end_date_str) formatted as "YYYY-MM-DD HH:MM"
    """
    today = datetime.today()
    time_start = time(start_hour, 0, 0)
    today_start = datetime.combine(today, time_start)
    date_start_dt = today_start + timedelta(days=days_ahead)
    date_end_dt = date_start_dt + timedelta(hours=duration_hours)

    date_start_str = date_start_dt.strftime("%Y-%m-%d %H:%M")
    date_end_str = date_end_dt.strftime("%Y-%m-%d %H:%M")

    return date_start_str, date_end_str


def test_commercial_can_create_event_cli(session, john_commercial, karim_contract):
    logged_user = john_commercial
    contract_repo = SqlalchemyContractRepository(session)

    # Sign the contract before creating it (required for event creation)
    karim_contract.sign_contract(updater_id=john_commercial.id)
    contract_repo.create(karim_contract)

    # Flush changes to make sure they're persisted in the session
    session.flush()

    date_start, date_end = generate_future_event_dates()

    user_input = (
        f"{karim_contract.id}\n"  # --contract-id
        "General assembly\n"  # --title
        f"{date_start}\n"  # --date-start (future date)
        f"{date_end}\n"  # --date-end (future date)
        "Banquet hall\n"  # --location
        "100\n"  # --attendees
        "General assembly for all employees\n"  # --notes
    )

    runner = CliRunner()

    result = runner.invoke(
        event,
        ["create"],
        input=user_input,
        obj={"session": session, "current_user": logged_user},
    )

    assert result.exit_code == 0
    assert "✅ Event General assembly created successfully" in result.output


def test_commercial_cannot_create_event_for_unsigned_contract_cli(session, john_commercial, karim_contract):
    logged_user = john_commercial
    contract_repo = SqlalchemyContractRepository(session)

    # Ensure the contract is NOT signed
    contract_repo.create(karim_contract)

    # Flush changes to make sure they're persisted in the session
    session.flush()

    date_start, date_end = generate_future_event_dates()

    user_input = (
        f"{karim_contract.id}\n"  # --contract-id
        "General assembly\n"  # --title
        f"{date_start}\n"  # --date-start (future date)
        f"{date_end}\n"  # --date-end (future date)
        "Banquet hall\n"  # --location
        "100\n"  # --attendees
        "General assembly for all employees\n"  # --notes
    )

    runner = CliRunner()

    result = runner.invoke(
        event,
        ["create"],
        input=user_input,
        obj={"session": session, "current_user": logged_user},
    )

    assert result.exit_code == 1
    assert "❌ Error creating event: Contract must be signed to create an event" in result.output


def test_commercial_cannot_create_event_with_past_date_cli(session, john_commercial, karim_contract):
    logged_user = john_commercial
    contract_repo = SqlalchemyContractRepository(session)

    # Sign the contract before creating it (required for event creation)
    karim_contract.sign_contract(updater_id=john_commercial.id)
    contract_repo.create(karim_contract)

    # Flush changes to make sure they're persisted in the session
    session.flush()

    user_input = (
        f"{karim_contract.id}\n"  # --contract-id
        "General assembly\n"  # --title
        "2025-01-01 14:00\n"  # --date-start (past date)
        "2025-01-01 18:00\n"  # --date-end (past date)
        "Banquet hall\n"  # --location
        "100\n"  # --attendees
        "General assembly for all employees\n"  # --notes
    )

    runner = CliRunner()

    result = runner.invoke(
        event,
        ["create"],
        input=user_input,
        obj={"session": session, "current_user": logged_user},
    )

    assert result.exit_code == 1
    assert "❌ Error creating event: Event start date must be in the future" in result.output
