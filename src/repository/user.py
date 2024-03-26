from src.models.user import UserModel
from src.utils.repository.sqlalchemy import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = UserModel


user_repository = UserRepository()
