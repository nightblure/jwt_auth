from fastapi import APIRouter, Depends

from src.core.auth.responses import InvalidTokenErrorResponse, ExpiredTokenErrorResponse
from src.deps import current_user
from src.users.schemas import AuthorizedUser

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.get(
    '/me',
    response_model=AuthorizedUser,
    responses={
        400: {"model": InvalidTokenErrorResponse},
        401: {"model": ExpiredTokenErrorResponse}
    }
)
def me(user: AuthorizedUser = Depends(current_user)):
    return user
