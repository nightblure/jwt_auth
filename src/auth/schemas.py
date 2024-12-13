from pydantic import BaseModel


class RegisterData(BaseModel):
    email: str
    username: str
    password: str


class LoginData(BaseModel):
    email: str
    password: str
