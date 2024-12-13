from datetime import datetime, timedelta
from datetime import timezone as tz
from typing import Any

import bcrypt
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidSignatureError

from src.auth.exceptions import ExpiredTokenError, InvalidTokenError


def make_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()


def verify_password(*, plain_password: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed.encode())


def create_jwt_token(
    *,
    payload: dict[str, Any],
    secret_key: str,
    algorithm: str,
    seconds_to_expire: int,
) -> str:
    payload.update(
        {
            "iat": datetime.now(tz=tz.utc),
            "exp": datetime.now(tz=tz.utc) + timedelta(seconds=seconds_to_expire),
        },
    )

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


def decode_jwt_token(*, token: str, secret_key: str, algorithm: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])  # type: ignore[no-any-return]
    except ExpiredSignatureError as e:
        raise ExpiredTokenError() from e
    except (DecodeError, InvalidSignatureError) as e:
        raise InvalidTokenError() from e
