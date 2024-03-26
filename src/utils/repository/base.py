from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from src.core.types import ID

T = TypeVar("T")


class RepositoryABC(Generic[T, ID], ABC):

    @abstractmethod
    async def get_by_id(self, id_: ID) -> T:
        """
        Найти одну запись по её ID

        :param id_: Id записи
        :raises MultipleResultsFound: Найдено больше одной записи
        :raises NoResultFound: Не найдено ни одной записи
        :return: Найденная запись
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, **filters) -> T:
        """
        Найти одну запись уникальным фильтрам

        :param filters: Kwargs для фильтрации
        :raises MultipleResultsFound: Найдено больше одной записи
        :raises NoResultFound: Не найдено ни одной записи
        :return: Найденная запись
        """
        raise NotImplementedError

    @abstractmethod
    async def exists(self, **filters) -> bool:
        """
        Проверяет есть ли такая запись

        :param filters: Kwargs для фильтрации
        :returns: True, если запись есть
        """
        raise NotImplementedError

    @abstractmethod
    async def filter(self, **filters: dict) -> list[T]:
        """
        Отфильтровать записи

        :param filters: kwargs для фильтрации
        :return: Список найденных записей
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, data: dict[str, Any]) -> T:
        """
        Создать новую запись

        :param data: Данные для создания записи
        :raises IntegrityError: Ошибка уникальности полей
        :return: Созданная запись
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, record_id: ID, data: dict[str, Any]) -> T:
        """
        Обновить запись

        :param record_id: Id старой записи
        :param data: Данные для обновления записи
        :raises IntegrityError: Ошибка уникальности полей
        :return: Обновлённая запись
        """
        raise NotImplementedError

    # @abstractmethod
    # async def delete(self, record_id: ID) -> None:
    #     """
    #     Удалить запись
    #
    #     :param record_id: Id записи для удаления
    #     :return: None
    #     """
    #     raise NotImplementedError
