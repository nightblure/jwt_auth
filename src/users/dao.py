from src.base_repository import BaseDAO
from src.db.models import User
from src.users.schemas import UserModel


class UserDAO(BaseDAO[User, UserModel]):
    model = User
    pydantic_model = UserModel
