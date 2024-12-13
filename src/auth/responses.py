from pydantic import BaseModel


class UserAlreadyRegisteredErrorResponse(BaseModel):
    detail: str = 'User with email "{user_email}" already exists'


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class InvalidCredentialsErrorResponse(BaseModel):
    detail: str = "Invalid user credentials"


class UserNotFoundErrorResponse(BaseModel):
    detail: str = "User not found"


class InvalidTokenErrorResponse(BaseModel):
    detail: str = "Invalid token"


class ExpiredTokenErrorResponse(BaseModel):
    detail: str = "The access token expired"
