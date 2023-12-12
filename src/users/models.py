import uuid

from sqlalchemy import Column, String

from src.core.db.db import Base


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, default=gen_uuid, primary_key=True)  # sqlite has no uuid type
    email = Column(String, unique=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
