from pydantic import BaseModel


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


class AuthorizedUser(BaseModel):
    email: str
    username: str
    logged_in: str
