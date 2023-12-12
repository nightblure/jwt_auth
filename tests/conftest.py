import os
import subprocess

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.app import app
from src.core.config import SRC_DIR
from src.core.db.db import get_sessionmaker
from src.deps import get_db_session
from src.users.repository import UserRepository
from tests.config import get_test_settings, DB_PATH


@pytest.fixture(scope='session')
def run_migrations():
    os.environ['TEST_MODE'] = '1'
    subprocess.run(f'cd {SRC_DIR}; alembic upgrade head', shell=True)


@pytest.fixture(scope='session')
def existed_user_db_data():
    return {
        'email': 'existed_user@gmail.com',
        'username': 'existed_user',
        'hashed_password': '$2b$12$7ThkIvhfCKKN1XUVD6H7YOd5nBIEa4/gu2hRrYy/Wn3QY1b/ny02W'
    }


@pytest.fixture(scope='session')
def fill_db(db_session, existed_user_db_data):
    r = UserRepository(db_session)
    r.create(existed_user_db_data)
    db_session.commit()


@pytest.fixture(scope='session', autouse=True)
def init(run_migrations, fill_db):
    yield
    os.remove(DB_PATH)


@pytest.fixture(scope='session')
def test_config():
    yield get_test_settings()


@pytest.fixture()
def api_client():
    return TestClient(app)


def db_session_dep() -> Session:
    db_url = get_test_settings().db_url
    session_cls = get_sessionmaker(db_url)
    session = session_cls()
    try:
        yield session
    finally:
        session.close()


db_session = pytest.fixture(scope='session')(db_session_dep)


@pytest.fixture(scope='session', autouse=True)
def override_deps():
    app.dependency_overrides[get_db_session] = db_session_dep


def user_repository(db_session):
    yield UserRepository(db_session)
