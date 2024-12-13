from src.base_repository import BaseSqlRepository
from src.db.models import User


class UserDAO(BaseSqlRepository[User]):
    model = User
