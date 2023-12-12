import time

import pytest

from src.core.auth.exceptions import ExpiredTokenError, InvalidTokenError
from src.core.auth.utils import create_jwt_token, decode_jwt_token


def test_decode_jwt_token_expired():
    secret_key = 'secret'
    algorithm = 'HS256'
    token = create_jwt_token(
        payload={'sub': 'test_user'},
        secret_key=secret_key,
        algorithm=algorithm,
        seconds_to_expire=1
    )

    time.sleep(1.5)

    with pytest.raises(ExpiredTokenError):
        decode_jwt_token(token, secret_key, algorithm)


def test_decode_jwt_token_invalid():
    secret_key = 'secret'
    algorithm = 'HS256'
    token = create_jwt_token(
        payload={'sub': 'test_user'},
        secret_key=secret_key,
        algorithm=algorithm,
        seconds_to_expire=60
    )

    with pytest.raises(InvalidTokenError):
        decode_jwt_token(token + 'rndinfo', secret_key, algorithm)
