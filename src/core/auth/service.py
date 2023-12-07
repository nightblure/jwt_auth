from datetime import datetime

from src.core.auth.exceptions import UserAlreadyRegisteredError, UserNotFoundError, InvalidCredentialsError
from src.core.auth.schemas import RegisterData, UserCreateModel, LoginData, UserModel, AuthorizedUser
from src.core.auth.utils import make_password_hash, create_jwt_token, is_password_equal_with_hash, decode_jwt_token
from src.core.config import Config
from src.users.repository import UserRepository


class AuthService:

    def __init__(self, user_repository: UserRepository, settings: Config):
        self.user_repository = user_repository
        self.secret_key = settings.jwt_secret
        self.jwt_algorithm = settings.jwt_algorithm

    def register(self, data: RegisterData):
        user = self.user_repository.one_or_none(field='email', value=data.email)

        if user is not None:
            raise UserAlreadyRegisteredError(data.email)

        user_db = UserCreateModel(
            email=data.email,
            username=data.username,
            hashed_password=make_password_hash(data.password)
        )
        self.user_repository.create(data=user_db)

    def login(self, login_data: LoginData) -> str:
        db_user = self.user_repository.one_or_none(field='email', value=login_data.email)

        if db_user is None:
            raise UserNotFoundError(status_code=404)

        user = UserModel.model_validate(db_user)

        if not is_password_equal_with_hash(password=login_data.password, hashed=user.hashed_password):
            raise InvalidCredentialsError(status_code=401)

        payload = {
            'sub': user.id,
            'email': user.email,
            'username': user.username,
        }

        return create_jwt_token(payload, self.secret_key, self.jwt_algorithm)

    def get_current_user(self, token: str):
        payload: dict = decode_jwt_token(token, self.secret_key, self.jwt_algorithm)
        username = payload['username']
        email = payload['email']
        logged_in = datetime.utcfromtimestamp(payload['iat']).strftime('%d-%m-%Y %H:%M:%S')
        return AuthorizedUser(email=email, username=username, logged_in=logged_in)
