from typing import Any

import pytest


@pytest.fixture
def register_data() -> dict[str, Any]:
    return {"email": "test@gmail.com", "username": "user", "password": "Qwerty123!"}


@pytest.fixture
def existed_user_register_data() -> dict[str, Any]:
    return {
        "email": "existed_user@gmail.com",
        "username": "existed_user",
        "password": "Qwerty123!",
    }
