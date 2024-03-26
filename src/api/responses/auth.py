from starlette import status

from src.api.error_code import AuthErrorCode
from src.core.types import OpenAPIResponseType
from src.schemas.error import ErrorSchema

REGISTER_POST_RESPONSES: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorSchema,
        "content": {
            "application/json": {
                "examples": {
                    AuthErrorCode.INVALID_PASSWORD: {
                        "summary": "Пароль не прошёл валидацию",
                        "value": {
                            "detail": {
                                "code": AuthErrorCode.INVALID_PASSWORD,
                                "reason": "Длина пароля должна быть больше 8 символов",
                                "error_fields": ["password"]
                            }
                        }
                    }
                }
            }
        }
    },
    status.HTTP_409_CONFLICT: {
        "model": ErrorSchema,
        "content": {
            "application/json": {
                "examples": {
                    AuthErrorCode.USER_ALREADY_EXISTS: {
                        "summary": "Пользователь с такими данными уже зарегистрирован",
                        "value": {
                            "detail": {
                                "code": AuthErrorCode.USER_ALREADY_EXISTS,
                                "reason": "Пользователь с такими данными уже зарегистрирован",
                                "error_fields": ["mail"]
                            }
                        }
                    },
                }
            }
        }
    }
}

LOGIN_POST_RESPONSES: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorSchema,
        "content": {
            "application/json": {
                "examples": {
                    AuthErrorCode.BAD_CREDENTIALS: {
                        "summary": "Не верные данные или пользователь не активен",
                        "value": {"detail": {
                            "code": AuthErrorCode.BAD_CREDENTIALS,
                            "reason": "Указан неверный логин или пароль",
                            "error_fields": None
                        }},
                    }
                }
            }
        },
    }
}