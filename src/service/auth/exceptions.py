from src.exceptions import ProjectException, ErrorFieldsMixin


class AuthServiceError(ProjectException):
    reason = "Ошибка аутентификации"


class UserAlreadyExists(ErrorFieldsMixin, ProjectException):
    reason = "Такой пользователь уже существует"


class InvalidPassword(AuthServiceError):
    reason = "Невалидный пароль"


class UserNotExists(AuthServiceError):
    reason = "Пользователь не найден"


class InvalidCredentials(AuthServiceError):
    reason = "Неверный email или пароль"
