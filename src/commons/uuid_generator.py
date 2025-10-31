from uuid import uuid4


class UuidGenerator:
    """UUID generator using Python's built-in uuid4 function."""

    def generate(self) -> str:
        return str(uuid4())
