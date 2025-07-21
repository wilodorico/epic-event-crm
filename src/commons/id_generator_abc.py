from abc import ABC, abstractmethod


class IdGeneratorABC(ABC):
    """Abstract base class for ID generators."""

    @abstractmethod
    def generate(self) -> str: ...
