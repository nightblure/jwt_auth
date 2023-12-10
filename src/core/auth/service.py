from datetime import datetime

from src.core.auth.exceptions import UserAlreadyRegisteredError, UserNotFoundError, InvalidCredentialsError
from src.core.auth.schemas import RegisterData, LoginData
from src.core.auth.utils import make_password_hash, create_jwt_token, verify_password, decode_jwt_token
from src.core.config import Config
from src.users.repository import UserRepository
from src.users.schemas import UserCreateModel, UserModel, AuthorizedUser


class AuthService:

    def __init__(self, user_repository: UserRepository, settings: Config):
        self.user_repository = user_repository
        self.secret_key = settings.jwt_secret
        self.seconds_to_expire = settings.seconds_to_expire
        self.jwt_algorithm = settings.jwt_algorithm

    def register(self, data: RegisterData) -> None:
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
            raise UserNotFoundError()

        user = UserModel.model_validate(db_user)

        if not verify_password(plain_password=login_data.password, hashed=user.hashed_password):
            raise InvalidCredentialsError()

        payload = {
            'sub': user.id,
            'email': user.email,
            'username': user.username,
        }

        return create_jwt_token(
            payload=payload,
            secret_key=self.secret_key,
            algorithm=self.jwt_algorithm,
            seconds_to_expire=self.seconds_to_expire
        )

    def get_current_user(self, token: str):
        payload: dict = decode_jwt_token(token, self.secret_key, self.jwt_algorithm)
        user_id: str = payload['sub']
        user = self.user_repository.one_or_none(value=user_id)
        logged_in = datetime.utcfromtimestamp(payload['iat']).strftime('%d-%m-%Y %H:%M:%S')
        return AuthorizedUser(email=user.email, username=user.username, logged_in=logged_in)
