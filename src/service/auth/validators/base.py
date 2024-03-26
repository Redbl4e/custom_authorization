from typing import Protocol


class ValidatorProtocol(Protocol):
    def validate(self, password: str):
        pass
