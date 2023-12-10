import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

SRC_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = SRC_DIR.parent
ENV_FILE = os.path.join(ROOT_DIR, '.env')

DB_URL = f'sqlite:///{SRC_DIR}/db.db'


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding='utf-8')

    db_url: str = DB_URL
    jwt_secret: str
    jwt_algorithm: str
    seconds_to_expire: int


app_settings = None


def get_settings():
    global app_settings

    if app_settings is None:
        app_settings = Config()

    return app_settings
