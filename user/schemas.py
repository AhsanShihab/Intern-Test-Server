from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str


class UserInDB(UserBase):
    id: str
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True
