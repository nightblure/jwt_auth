import subprocess

from src.core.config import SRC_DIR
from src.core.db.db import db_session
from src.users.repository import UserRepository


def init_db():
    subprocess.run(f'cd {SRC_DIR}; alembic upgrade head', shell=True)
    with db_session() as session:
        r = UserRepository(session)
        r.create({'email': 'eemail@gmail.com', 'username': 'vanya', 'hashed_password': ''})
        session.commit()


if __name__ == '__main__':
    init_db()
