from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

SRC_DIR = Path(__file__).resolve().parent


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    db_url: str = f"sqlite:///{SRC_DIR}/db.db"
    jwt_secret: str
    jwt_algorithm: str
    seconds_to_expire: int

    db_path: str = str(SRC_DIR / "db.db")
