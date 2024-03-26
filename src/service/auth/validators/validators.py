import gzip
from functools import cached_property
from pathlib import Path
from src.service.auth.validators.exceptions import PasswordValidationError


class MinimumLengthValidator:
    """
    Валидация пароля по длине
    """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password: str):
        if len(password) < self.min_length:
            raise PasswordValidationError(
                reason=f"Длина пароля должна быть "
                       f"больше {self.min_length} символов"
            )


class CommonPasswordValidator:
    """
    Валидация пароля на распространенность
    """

    def __init__(self):
        password_list_path = self.default_password_list_path
        try:
            with gzip.open(password_list_path, "rt", encoding="utf-8") as f:
                self.passwords = {x.strip() for x in f}
        except OSError:
            with open(password_list_path) as f:
                self.passwords = {x.strip() for x in f}

    def validate(self, password: str):
        if password.lower().strip() in self.passwords:
            raise PasswordValidationError(
                reason="Пароль слишком распространенный"
            )

    @cached_property
    def default_password_list_path(self):
        return Path(__file__).resolve().parent / "common-passwords.txt.gz"


class NumericPasswordValidator:
    """Проверяет, чтобы пароль состоял не только из цифр"""

    def validate(self, password: str):
        if password.isdigit():
            raise PasswordValidationError(
                reason="Пароль состоит только из цифр"
            )
