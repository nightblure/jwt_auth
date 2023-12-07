from fastapi import HTTPException


class UserAlreadyRegisteredError(HTTPException):
    status_code = 409

    def __init__(self, user_email: str):
        self.detail = f'User with email "{user_email}" already exists'


class UserNotFoundError(HTTPException):
    def __init__(self, status_code):
        self.status_code = status_code
        self.detail = 'User not found'


class InvalidCredentialsError(HTTPException):
    def __init__(self, status_code):
        self.status_code = status_code
        self.detail = 'Invalid credentials'
