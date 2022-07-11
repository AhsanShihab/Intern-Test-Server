from fastapi import APIRouter, Depends, Query
from .schemas import TweetCreate, Tweet, ListTweets
from common_schemas import Unauthorized, Forbidden, NotFound
from dependencies import require_token, get_current_user
from . import service

router = APIRouter(
    prefix="/api/tweets",
    tags=["Tweets"],
    dependencies=[Depends(require_token)],
    responses={401: {"description": "Unauthorized", "model": Unauthorized}},
)


@router.get("", response_model=ListTweets)
async def get_tweets(skip: int = Query(default=0), limit: int = Query(default=5)):
    return await service.get_tweets(skip=skip, limit=limit)


@router.post("", status_code=201, response_model=Tweet)
async def create_tweet(tweet: TweetCreate, user=Depends(get_current_user)):
    return await service.create_tweet(data=tweet, user=user)


@router.get(
    "/{tweet_id}",
    response_model=Tweet,
    responses={404: {"description": "Not Found", "model": NotFound}},
)
async def get_tweets_by_id(tweet_id: int):
    return await service.get_tweets_by_id(tweet_id)


@router.put(
    "/{tweet_id}",
    response_model=Tweet,
    responses={
        403: {"description": "Forbidden", "model": Forbidden},
        404: {"description": "Not Found", "model": NotFound},
    },
)
async def update_tweet(
    tweet_id: int, tweet: TweetCreate, user=Depends(get_current_user)
):
    return await service.update_tweet(tweet_id, tweet, user.id)


@router.delete(
    "/{tweet_id}",
    status_code=204,
    responses={
        403: {"description": "Forbidden", "model": Forbidden},
        404: {"description": "Not Found", "model": NotFound},
    },
)
async def delete_tweet(tweet_id: int, user=Depends(get_current_user)):
    await service.delete_tweet_by_id(tweet_id, user.id)
    return
