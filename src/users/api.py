from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.auth.schemas import UserModel, AuthorizedUser
from src.core.auth.service import AuthService
from src.deps import current_user, get_auth_service

users_router = APIRouter(prefix='/users', tags=['users'])


# user: UserModel = Depends(current_user)
@users_router.get('/me', response_model=AuthorizedUser)
def me(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        auth_service: AuthService = Depends(get_auth_service)
):
    user = auth_service.get_current_user(credentials.credentials)
    return user
