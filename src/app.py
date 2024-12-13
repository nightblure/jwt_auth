from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.api import auth_router
from src.di import di_container
from src.users.api import users_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    _ = di_container
    yield


def create_app() -> FastAPI:
    app_ = FastAPI(lifespan=lifespan)
    app_.include_router(auth_router)
    app_.include_router(users_router)
    return app_


app = create_app()
