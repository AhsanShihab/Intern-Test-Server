from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.future import select
from database import BaseModel
from authentication.security_config import pwd_context


class User(BaseModel):
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    tweets = relationship("Tweet", back_populates="author")

    @classmethod
    async def create(cls, data: dict, session=None):
        data_copy = data.copy()
        password = data["password"]
        del data_copy["password"]

        hashed_password = pwd_context.hash(password)
        return await super().create(
            data={**data_copy, "hashed_password": hashed_password},
            session=session,
        )

    @classmethod
    async def get_by_username(cls, username: str, session=None):
        async with cls.session_handler(session) as session:
            stm = select(cls).filter(cls.username == username)
            res = (await session.execute(stm)).scalars().first()
        return res
