import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def str_uuid_factory() -> str:
    return str(uuid.uuid4())


class Base(DeclarativeBase): ...


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        default=str_uuid_factory,
        primary_key=True,
    )  # sqlite hasn't uuid type
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str]
    hashed_password: Mapped[str]
