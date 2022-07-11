from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union
from database import BaseModel


class Token(BaseModel):
    refresh_token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, unique=True)

    @classmethod
    async def store_token(
        cls, user_id: str, refresh_token: str, session: Union[AsyncSession, None] = None
    ):
        async with cls.session_handler(session) as session:
            stm = select(cls).filter(cls.user_id == user_id)
            token = (await session.execute(stm)).scalars().first()
            if not token:
                await cls.create(
                    {"user_id": user_id, "refresh_token": refresh_token},
                    session=session,
                )
            else:
                await cls.update(
                    token.id, {"refresh_token": refresh_token}, session=session
                )

    @classmethod
    async def find_token_entry(
        cls, refresh_token, session: Union[AsyncSession, None] = None
    ):
        async with cls.session_handler(session) as session:
            stm = select(cls).filter(cls.refresh_token == refresh_token)
            token = (await session.execute(stm)).scalars().first()
            return token
