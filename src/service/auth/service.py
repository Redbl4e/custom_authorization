from typing import Optional
from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from src.core.types import UP
from src.repository.user import user_repository, UserRepository
from src.schemas.user import UserCreateSchema
from src.service.auth.exceptions import (
    UserAlreadyExists,
    InvalidPassword, UserNotExists, InvalidCredentials
)
from src.service.auth.password_helper import (
    PasswordHelperABC,
    passlib_password_helper
)
from src.service.auth.validators.base import ValidatorProtocol
from src.service.auth.validators.exceptions import PasswordValidationError
from src.service.auth.validators.validators import (
    CommonPasswordValidator,
    NumericPasswordValidator,
    MinimumLengthValidator
)
from src.utils.repository.base import RepositoryABC
from src.utils.repository.exceptions import IntegrityError, RepositoryException


class UserService:

    def __init__(
            self,
            user_repo: Optional[RepositoryABC[UP, UUID]] = None,
            password_helper: Optional[PasswordHelperABC] = None,
    ):
        self.user_repo = user_repo if user_repo else UserRepository()
        self.password_helper = (
            password_helper if password_helper else passlib_password_helper
        )

    async def get_user_by_id(self, id_: UUID) -> UP:
        """Поиск пользователя по UUID
        :param id_: UUID пользователя
        :raises UserNotExists: Пользователь не найден
        :return: Пользователь
        """
        try:
            user = await self.user_repo.get(id=id_)
        except RepositoryException as e:
            raise UserNotExists(reason=e.reason)
        return user

    async def get_user_by_email(self, email: EmailStr) -> UP:
        """Поиск пользователя по email
        :param email: Email адрес пользователя
        :raises UserNotExists: Пользователь не найден
        :return: Пользователь
        """
        try:
            user = await self.user_repo.get(email=email)
        except RepositoryException as e:
            raise UserNotExists(reason=e.reason)
        return user

    async def create(self, user_data: UserCreateSchema) -> UP:
        """
        Создание пользователя и добавление в БД
        :param user_data: Pydantic схема для создания пользователя
        :raise UserAlreadyExists: пользователь уже зарегистрирован со схожими данными
        :raise InvalidPassword: Пароль не валидный
        :return: Созданный пользователь
        """
        user_dict = user_data.model_dump()
        password = user_dict.pop("password")

        await self.validate_password(user_data.password)

        user_dict["hashed_password"] = self.password_helper.hash(password)
        try:
            created_user = await self.user_repo.create(user_dict)
        except IntegrityError as e:
            raise UserAlreadyExists(
                error_fields=e.error_fields)
        return created_user

    async def authenticate(
            self, credentials: OAuth2PasswordRequestForm
    ) -> UP:
        """
        Аутентифицирует пользователя по его email/password

        :param credentials: Данные для входа
        :raises InvalidCredentials: Email/пароль не валидны
        :return: Пользователь
        """
        try:
            user = await self.get_user_by_email(credentials.username)
        except UserNotExists:
            # Запуск хеширования, чтобы избежать timing-атаки
            self.password_helper.hash(credentials.password)
            raise InvalidCredentials()
        password_match, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if password_match is False:
            raise InvalidCredentials()

        if updated_password_hash:
            await self.user_repo.update(
                user.id, {"hashed_password": updated_password_hash}
            )
        return user

    async def validate_password(self, password: str) -> None:
        """
        Валидация пароля

        :param password: Пароль для валидации
        :raises InvalidPassword: Пароль не валидный
        :return: `None`, если пароль валидный
        """
        # if settings.DEBUG:
        #     return
        for validator in self.password_validators:
            try:
                validator.validate(password)
            except PasswordValidationError as e:
                raise InvalidPassword(
                    reason=e.reason
                )

    @property
    def password_validators(self) -> list[ValidatorProtocol]:
        validators = [
            MinimumLengthValidator, NumericPasswordValidator,
            CommonPasswordValidator
        ]
        return [class_() for class_ in validators]


async def get_user_service() -> UserService:
    yield UserService(
        user_repository,
        passlib_password_helper
    )
