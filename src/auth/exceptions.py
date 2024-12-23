from fastapi import HTTPException


class UserAlreadyRegisteredError(HTTPException):
    status_code = 409

    def __init__(self, user_email: str) -> None:
        self.detail = f'User with email "{user_email}" already exists'


class UserNotFoundError(HTTPException):
    def __init__(self) -> None:
        self.status_code = 404
        self.detail = "User not found"


class InvalidCredentialsError(HTTPException):
    def __init__(self) -> None:
        self.status_code = 401
        self.detail = "Invalid credentials"


class InvalidTokenError(HTTPException):
    def __init__(self) -> None:
        self.status_code = 400
        self.detail = "Invalid token"


class ExpiredTokenError(HTTPException):
    def __init__(self) -> None:
        self.status_code = 401
        self.detail = "The access token expired"
