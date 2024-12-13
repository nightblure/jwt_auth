from collections.abc import Callable

from sqlalchemy.orm import Session


def db_session_resource(session_factory: Callable[..., Session]) -> Session:
    session = session_factory()
    return session


# @contextmanager
# def db_session_resource(session_factory: Callable[..., Session]) -> Iterator[Session]:
#     session = session_factory()
#
#     try:
#         yield session
#     finally:
#         session.close()
