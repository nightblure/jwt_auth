from typing import Any

from fastapi import APIRouter
from injection import inject
from starlette import status

from src.auth.responses import (
    InvalidCredentialsErrorResponse,
    LoginResponse,
    UserAlreadyRegisteredErrorResponse,
    UserNotFoundErrorResponse,
)
from src.auth.schemas import LoginData, RegisterData
from src.di import AuthServiceDep

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/register",
    responses={409: {"model": UserAlreadyRegisteredErrorResponse}},
    status_code=status.HTTP_201_CREATED,
)
@inject  # type: ignore[misc]
def register(
    register_data: RegisterData,
    auth_service: AuthServiceDep,
) -> dict[str, Any]:
    auth_service.register(register_data)
    return {}


@auth_router.post(
    "/login",
    responses={
        401: {"model": InvalidCredentialsErrorResponse},
        404: {"model": UserNotFoundErrorResponse},
    },
    response_model=LoginResponse,
)
@inject
def login(
    login_data: LoginData,
    auth_service: AuthServiceDep,
) -> dict[str, Any]:
    access_token = auth_service.login(login_data)
    return {"access_token": access_token}
