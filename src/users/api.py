from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from injection import inject

from src.auth.responses import ExpiredTokenErrorResponse, InvalidTokenErrorResponse
from src.di import AuthServiceDep
from src.users.schemas import AuthorizedUser

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get(
    "/me",
    response_model=AuthorizedUser,
    responses={
        400: {"model": InvalidTokenErrorResponse},
        401: {"model": ExpiredTokenErrorResponse},
    },
)
@inject  # type: ignore[misc]
def me(
    auth_service: AuthServiceDep,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),  # noqa: B008
) -> dict[str, Any]:
    user = auth_service.get_current_user(credentials.credentials)
    return {"email": user.email, "username": user.username, "logged_in": user.logged_in}
