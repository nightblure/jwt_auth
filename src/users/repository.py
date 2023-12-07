from src.base_repository import BaseSqlRepository
from src.users.models import User


class UserRepository(BaseSqlRepository):
    model = User
