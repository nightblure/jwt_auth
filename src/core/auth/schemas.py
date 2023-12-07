from datetime import datetime

from pydantic import BaseModel


class RegisterData(BaseModel):
    email: str
    username: str
    password: str


class UserCreateModel(BaseModel):
    email: str
    username: str
    hashed_password: str


class UserModel(BaseModel):
    id: str
    email: str
    username: str
    hashed_password: str

    class Config:
        from_attributes = True


class LoginData(BaseModel):
    email: str
    password: str


class AuthorizedUser(BaseModel):
    email: str
    username: str
    logged_in: str
