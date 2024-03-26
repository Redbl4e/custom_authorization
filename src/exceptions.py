
class ProjectException(Exception):
    reason = "Ошибка проекта"

    def __init__(self, reason: str | None = None):
        if reason:
            self.reason = reason

    def __str__(self):
        return self.reason


class ErrorFieldsMixin:
    error_fields: list[str]

    def __init__(self, *args, error_fields: list[str], **kwargs):
        super().__init__(*args, **kwargs)
        self.error_fields = error_fields
