from abc import ABC, abstractmethod
from datetime import datetime


class ClockABC(ABC):
    """Abstract base class for clock implementations."""

    @abstractmethod
    def now(self) -> datetime:
        pass
