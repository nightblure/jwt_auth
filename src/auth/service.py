from datetime import datetime

from src.auth.exceptions import (
    InvalidCredentialsError,
    UserAlreadyRegisteredError,
    UserNotFoundError,
)
from src.auth.schemas import LoginData, RegisterData
from src.auth.utils import (
    create_jwt_token,
    decode_jwt_token,
    make_password_hash,
    verify_password,
)
from src.users.dao import UserDAO
from src.users.schemas import AuthorizedUser, UserCreateModel, UserModel


class AuthService:
    def __init__(
        self,
        *,
        user_dao: UserDAO,
        secret_key: str,
        seconds_to_expire: int,
        jwt_algorithm: str,
    ) -> None:
        self.user_dao = user_dao
        self.secret_key = secret_key
        self.jwt_algorithm = jwt_algorithm
        self.seconds_to_expire = seconds_to_expire

    def register(self, data: RegisterData) -> None:
        user = self.user_dao.one_or_none(field="email", value=data.email)

        if user is not None:
            raise UserAlreadyRegisteredError(data.email)

        user_db = UserCreateModel(
            email=data.email,
            username=data.username,
            hashed_password=make_password_hash(data.password),
        )

        self.user_dao.create(user_db)
        self.user_dao.commit()

    def login(self, login_data: LoginData) -> str:
        db_user = self.user_dao.one_or_none(field="email", value=login_data.email)

        if db_user is None:
            raise UserNotFoundError()

        user = UserModel.model_validate(db_user)

        if not verify_password(
            plain_password=login_data.password,
            hashed=user.hashed_password,
        ):
            raise InvalidCredentialsError()

        payload = {
            "sub": user.id,
            "email": user.email,
            "username": user.username,
        }

        return create_jwt_token(
            payload=payload,
            secret_key=self.secret_key,
            algorithm=self.jwt_algorithm,
            seconds_to_expire=self.seconds_to_expire,
        )

    def get_current_user(self, token: str) -> AuthorizedUser:
        payload = decode_jwt_token(token=token, secret_key=self.secret_key, algorithm=self.jwt_algorithm)

        user_id: str = payload["sub"]
        user: UserModel = self.user_dao.one_or_none(value=user_id)  # type: ignore[assignment]
        logged_in = datetime.fromtimestamp(payload["iat"]).strftime("%d-%m-%Y %H:%M:%S")

        return AuthorizedUser(
            email=user.email,
            username=user.username,
            logged_in=logged_in,
        )
