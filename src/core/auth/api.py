from fastapi import APIRouter, Depends, Response
import starlette.status as status

from src.core.auth.responses import (
    UserAlreadyRegisteredErrorResponse,
    LoginResponse,
    InvalidCredentialsErrorResponse,
    UserNotFoundErrorResponse
)
from src.core.auth.schemas import RegisterData, LoginData
from src.core.auth.service import AuthService
from src.deps import get_auth_service

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post(
    '/register',
    responses={409: {"model": UserAlreadyRegisteredErrorResponse}},
    status_code=status.HTTP_201_CREATED
)
def register(register_data: RegisterData, service: AuthService = Depends(get_auth_service)):
    service.register(register_data)
    return Response(status_code=status.HTTP_201_CREATED)


@auth_router.post(
    '/login',
    responses={
        401: {"model": InvalidCredentialsErrorResponse},
        404: {"model": UserNotFoundErrorResponse}
    },
    response_model=LoginResponse
)
def login(login_data: LoginData, service: AuthService = Depends(get_auth_service)):
    return {'access_token': service.login(login_data)}
