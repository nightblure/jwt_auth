import pytest


@pytest.fixture()
def register_data():
    return {
        "email": "test@gmail.com",
        "username": "vanya",
        "password": "Qwerty123!"
    }


@pytest.fixture()
def existed_user_register_data():
    return {
        'email': 'existed_user@gmail.com',
        'username': 'existed_user',
        'password': 'Qwerty123!'
    }
