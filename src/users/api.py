from fastapi import APIRouter, Depends

from src.deps import current_user
from src.users.schemas import AuthorizedUser

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.get('/me', response_model=AuthorizedUser)
def me(user: AuthorizedUser = Depends(current_user)):
    return user
