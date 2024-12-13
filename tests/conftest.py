from collections.abc import Iterator
from typing import Any

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from src.app import create_app
from src.config import Config
from src.db.models import Base
from src.di import DIContainer
from src.di import di_container as _di_container


@pytest.fixture(scope="session")
def existed_user_db_data() -> dict[str, Any]:
    return {
        "email": "existed_user@gmail.com",
        "username": "existed_user",
        "hashed_password": "$2b$12$7ThkIvhfCKKN1XUVD6H7YOd5nBIEa4/gu2hRrYy/Wn3QY1b/ny02W",
    }


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_app()


@pytest.fixture(scope="session", autouse=True)
def api_client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def di_container() -> DIContainer:
    return _di_container


@pytest.fixture(scope="session")
def overrides() -> dict[str, Any]:
    test_config = Config(
        jwt_secret="gG*(WYT8734y5rhfs8T&G",
        jwt_algorithm="HS256",
        seconds_to_expire=3600,
    )
    return {
        "config": test_config,
    }


@pytest.fixture(scope="session", autouse=True)
def override_dependencies(
    di_container: DIContainer,
    overrides: dict[str, Any],
) -> Iterator[None]:
    with di_container.override_providers(overrides):
        yield


@pytest.fixture(scope="session", autouse=True)
def tests_lifespan(di_container: DIContainer, existed_user_db_data: dict[str, Any]) -> None:
    db_session = di_container.db_session()
    meta = Base.metadata

    for table in reversed(meta.sorted_tables):
        db_session.execute(table.delete())

    db_session.commit()
    db_session.close()

    user_dao = di_container.user_dao()
    user_dao.create(existed_user_db_data)
