from enum import StrEnum


class AuthErrorCode(StrEnum):
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    USER_NOT_EXIST = "USER_NOT_EXIST"
    USER_PASSWORD_MATCH = "USER_PASSWORD_MATCH"
    USER_PASSWORD_MISMATCH = "USER_PASSWORD_MISMATCH"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    BAD_CREDENTIALS = "BAD_CREDENTIALS"

