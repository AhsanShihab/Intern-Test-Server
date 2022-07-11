import os
import uuid
from datetime import timedelta
from fastapi import HTTPException, status
from user.models import User
from .models import Token
from .security_config import (
    pwd_context,
    create_token,
    decode_token,
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def create_toke_pair(user: User):
    access_token_expires = timedelta(minutes=os.environ.get("ACCESS_TOKEN_TTL", 15))
    access_token = create_token(
        data={"user": user.username, "id": user.id},
        expires_delta=access_token_expires,
    )

    refresh_token = create_token(data={"id": user.id, "hash": str(uuid.uuid4())})
    await Token.store_token(user_id=user.id, refresh_token=refresh_token)

    return access_token, refresh_token


async def authenticate_user(username: str, password: str):
    user = await User.get_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def login_user(username: str, password: str):
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token, refresh_token = await create_toke_pair(user)
    return access_token, refresh_token


async def refresh_tokens(refresh_token: str):
    token_entry = await Token.find_token_entry(refresh_token)
    if token_entry is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid refresh token",
        )
    decoded_token = decode_token(refresh_token)
    user: User = await User.get_by_id(decoded_token["id"])
    access_token, refresh_token = await create_toke_pair(user)
    return access_token, refresh_token
