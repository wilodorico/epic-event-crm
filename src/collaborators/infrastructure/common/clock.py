from datetime import datetime

from commons.clock_abc import ClockABC


class Clock(ClockABC):
    """Concrete implementation of ClockABC using the system clock."""

    def now(self) -> datetime:
        return datetime.now()
