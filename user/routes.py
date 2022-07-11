from typing import List
from fastapi import APIRouter, Query, HTTPException, status
from common_schemas import NotFound
from .schemas import UserCreate, UserRead
from . import service

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("", response_model=List[UserRead])
async def list_users(skip: int = Query(default=0), limit: int = Query(default=5)):
    return await service.list_users(skip=skip, limit=limit)


@router.post("", response_model=UserRead)
async def create_user(payload: UserCreate):
    return await service.create_user(payload)


@router.get(
    "/{user_id}",
    response_model=UserRead,
    responses={404: {"description": "Not Found", "model": NotFound}},
)
async def get_user_by_id(user_id: int):
    user = await service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
