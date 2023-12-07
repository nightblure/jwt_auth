from datetime import datetime, timedelta

import bcrypt
import jwt


def make_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()


def is_password_equal_with_hash(*, password: str, hashed: str):
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_jwt_token(payload: dict, secret_key: str, algorithm: str):
    payload.update({
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1)
    })

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


def decode_jwt_token(token: str, secret_key: str, algorithm: str):
    return jwt.decode(token, secret_key, algorithms=algorithm)
