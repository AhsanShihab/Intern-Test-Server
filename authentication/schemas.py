from pydantic import BaseModel
from typing import Union


class Credentials(BaseModel):
    username: str
    password: str


class TokenRefreshPayload(BaseModel):
    refresh_token: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    id: str
    hashed_password: str
