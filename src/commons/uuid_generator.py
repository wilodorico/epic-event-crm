from uuid import uuid4


class UuidGenerator:
    def generate(self) -> str:
        return str(uuid4())
