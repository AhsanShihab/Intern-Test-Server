from fastapi import APIRouter
from .schemas import Token, Credentials, TokenRefreshPayload
from . import service

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("", response_model=Token)
async def login(credentials: Credentials):
    access_token, refresh_token = await service.login_user(
        credentials.username, credentials.password
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/token", response_model=Token)
async def refresh_token(payload: TokenRefreshPayload):
    access_token, refresh_token = await service.refresh_tokens(
        refresh_token=payload.refresh_token
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
