class FixedIdGenerator:
    def __init__(self, hardcoded_id: str = "id-1"):
        self.hardcoded_id = hardcoded_id

    def generate(self) -> str:
        return self.hardcoded_id
