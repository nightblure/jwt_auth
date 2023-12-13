import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

SRC_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = SRC_DIR.parent

APP_ENV_FILE = os.path.join(ROOT_DIR, '.env')
APP_DB_URL = f'sqlite:///{SRC_DIR}/db.db'

TESTS_DIR = os.path.join(ROOT_DIR, 'tests')
TESTS_ENV_FILE = os.path.join(TESTS_DIR, '.env_test')
TESTS_DB_URL = f'sqlite:///{TESTS_DIR}/db.db'
TESTS_DB_PATH = os.path.join(TESTS_DIR, 'db.db')

DB_URL = APP_DB_URL
ENV_FILE = APP_ENV_FILE

if os.environ.get('TEST_MODE') is not None:
    DB_URL = TESTS_DB_URL
    ENV_FILE = TESTS_ENV_FILE


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding='utf-8')

    db_url: str = DB_URL
    jwt_secret: str
    jwt_algorithm: str
    seconds_to_expire: int


def get_settings():
    return Config()
