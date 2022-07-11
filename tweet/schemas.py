from pydantic import BaseModel
from typing import List
from datetime import datetime
from user.schemas import UserRead


class TweetCreate(BaseModel):
    text: str


class Tweet(BaseModel):
    id: int
    text: str
    author: UserRead
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


ListTweets = List[Tweet]
