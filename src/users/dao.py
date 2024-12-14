from src.base_repository import BaseDAO
from src.db.models import User


class UserDAO(BaseDAO[User]):
    model = User
