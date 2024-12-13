from typing import Annotated

from fastapi import Depends
from injection import DeclarativeContainer, Provide, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.auth.service import AuthService
from src.config import Config
from src.db.session import db_session_resource
from src.users.dao import UserDAO


class DIContainer(DeclarativeContainer):  # type: ignore[misc]
    config = providers.Singleton(Config)

    db_engine = providers.Singleton(
        create_engine,
        url=config.provided.db_url,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=False,
    )

    session_factory = providers.Singleton(
        sessionmaker,
        db_engine,
        autocommit=False,
        autoflush=False,
    )

    db_session = providers.Transient(
        db_session_resource,
        session_factory,
        # function_scope=True
    )

    user_dao = providers.Transient(
        UserDAO,
        db_session=db_session.cast,
    )

    auth_service = providers.Transient(
        AuthService,
        user_dao=user_dao.cast,
        secret_key=config.provided.jwt_secret,
        jwt_algorithm=config.provided.jwt_algorithm,
        seconds_to_expire=config.provided.seconds_to_expire,
    )


di_container: DIContainer = DIContainer()
AuthServiceDep = Annotated[AuthService, Depends(Provide[di_container.auth_service])]
