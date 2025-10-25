from datetime import datetime

from commons.clock_abc import ClockABC


class FakeClock(ClockABC):
    """Fake clock implementation for testing purposes."""

    def __init__(self, fixed_datetime: datetime):
        self._fixed_datetime = fixed_datetime

    def now(self) -> datetime:
        return self._fixed_datetime
