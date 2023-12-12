from datetime import datetime, timedelta

import bcrypt
import jwt

from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError

from src.core.auth.exceptions import ExpiredTokenError, InvalidTokenError


def make_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()


def verify_password(*, plain_password: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed.encode())


def create_jwt_token(*, payload: dict, secret_key: str, algorithm: str, seconds_to_expire: int) -> str:
    payload.update({
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=seconds_to_expire)
    })

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


def decode_jwt_token(token: str, secret_key: str, algorithm: str) -> dict:
    try:
        return jwt.decode(token, secret_key, algorithms=algorithm)
    except ExpiredSignatureError:
        raise ExpiredTokenError()
    except (DecodeError, InvalidSignatureError):
        raise InvalidTokenError()
