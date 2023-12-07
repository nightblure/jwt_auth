from contextlib import contextmanager
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.auth.service import AuthService
from src.core.config import get_settings
from src.core.db.db import SessionLocal
from src.users.repository import UserRepository


def get_db_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


DbSession = Annotated[Session, Depends(get_db_session)]

"""
For direct session using
Example:
    with db_session() as session:
        ...
"""
db_session = contextmanager(get_db_session)


def get_user_repository(session: DbSession):
    return UserRepository(session)


def get_auth_service(user_repository=Depends(get_user_repository)):
    return AuthService(user_repository=user_repository, settings=get_settings())


def current_user():
    pass