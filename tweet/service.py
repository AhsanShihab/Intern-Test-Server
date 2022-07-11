from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
from user.schemas import UserInDB
from .schemas import TweetCreate
from .models import Tweet


async def get_tweets(skip, limit):
    return await Tweet.list_all(
        skip=skip, limit=limit, options=[selectinload(Tweet.author)]
    )


async def get_tweets_by_id(id: int):
    tweet = await Tweet.get_by_id(id, options=[selectinload(Tweet.author)])
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Tweet not found"}
        )
    return tweet


async def create_tweet(user: UserInDB, data: TweetCreate):
    new_tweet = await Tweet.create(
        {
            "author_id": user.id,
            "text": data.text,
        },
        select_options=[selectinload(Tweet.author)],
    )

    return new_tweet


async def update_tweet(tweet_id: int, update: TweetCreate, user_id: str):
    tweet = await Tweet.get_by_id(tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Tweet not found"}
        )
    if tweet.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "You don't have permission to update this tweet"},
        )
    return await Tweet.update(
        tweet_id, {"text": update.text}, select_options=[selectinload(Tweet.author)]
    )


async def delete_tweet_by_id(tweet_id: int, user_id: str):
    tweet = await Tweet.get_by_id(tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "Tweet not found"}
        )
    if tweet.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "You don't have permission to delete this tweet"},
        )

    return await Tweet.delete_by_id(tweet_id)
