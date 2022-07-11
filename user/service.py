from .models import User
from .schemas import UserCreate


async def list_users(skip, limit):
    return await User.list_all(skip=skip, limit=limit)


async def create_user(user: UserCreate):
    return await User.create(user.dict())


async def get_user_by_id(id: int):
    return await User.get_by_id(id)
