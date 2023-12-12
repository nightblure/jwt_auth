import os

from pydantic_settings import SettingsConfigDict

from src.core.config import Config, ROOT_DIR

TESTS_DIR = os.path.join(ROOT_DIR, 'tests')
TESTS_ENV_FILE = os.path.join(TESTS_DIR, '.env_test')

DB_URL = f'sqlite:///{TESTS_DIR}/db.db'
DB_PATH = os.path.join(TESTS_DIR, 'db.db')


class TestConfig(Config):
    model_config = SettingsConfigDict(env_file=TESTS_ENV_FILE, env_file_encoding='utf-8')

    db_url: str = DB_URL


def get_test_settings():
    return TestConfig()
