import os
import datetime
import functools
import inflect
from typing import List, Union, Any
from contextlib import asynccontextmanager
from sqlalchemy import Column, Integer, DateTime, update, insert, desc, delete
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base, declared_attr

pluralize = inflect.engine().plural

SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DB_URL", "postgresql+asyncpg://postgres:password123@localhost:5432"
)

print('using SQLALCHEMY_DATABASE_URL:', SQLALCHEMY_DATABASE_URL)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, class_=AsyncSession
)


class BaseModel(object):
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    @declared_attr
    def __tablename__(cls):
        return pluralize(cls.__name__.lower())

    @staticmethod
    @asynccontextmanager
    async def session_handler(session: Union[AsyncSession, None] = None):
        is_self_created_session = False
        try:
            if not session:
                session = async_session()
                is_self_created_session = True

            yield session
        finally:
            if is_self_created_session:
                await session.close()

    @classmethod
    async def list_all(
        cls,
        skip=0,
        limit=10,
        session: Union[AsyncSession, None] = None,
        options: List[Any] = [],
    ):
        stm = select(cls).order_by(desc(cls.created_at)).offset(skip).limit(limit)
        if len(options):
            stm = stm.options(*options)
        async with cls.session_handler(session) as session:
            res = (await session.execute(stm)).scalars().all()

        return res

    @classmethod
    async def get_by_id(
        cls, id, session: Union[AsyncSession, None] = None, options: List[Any] = []
    ):
        stm = select(cls).filter(cls.id == id)
        if len(options):
            stm = stm.options(*options)
        async with cls.session_handler(session) as session:
            res = (await session.execute(stm)).scalars().first()
        return res

    @classmethod
    async def create(
        cls,
        data: dict,
        session: Union[AsyncSession, None] = None,
        select_options: List[Any] = [],
    ):
        obj = cls(**data)

        async with cls.session_handler(session) as session:
            stm_1 = insert(cls).values(**data).returning(cls.id)
            new_entry_id = (await session.execute(stm_1)).scalars().first()
            await session.commit()
            stm_2 = select(cls).where(cls.id == new_entry_id)
            if len(select_options):
                stm_2 = stm_2.options(*select_options)
            obj = (await session.execute(stm_2)).scalars().first()

        return obj

    @classmethod
    async def update(
        cls,
        id,
        data: dict,
        session: Union[AsyncSession, None] = None,
        select_options: List[Any] = [],
    ):
        async with cls.session_handler(session) as session:
            stm_1 = update(cls).where(cls.id == id).values(**data).returning(cls.id)
            (await session.execute(stm_1)).scalars().first()
            await session.commit()
            stm_2 = select(cls).where(cls.id == id)
            if len(select_options):
                stm_2 = stm_2.options(*select_options)
            obj = (await session.execute(stm_2)).scalars().first()

        return obj

    @classmethod
    async def delete_by_id(cls, id, session: Union[AsyncSession, None] = None):
        stm = delete(cls).where(cls.id == id)
        async with cls.session_handler(session) as session:
            res = await session.execute(stm)
            await session.commit()
        return res


BaseModel = declarative_base(cls=BaseModel)


def use_session():
    def wrapper(fn):
        @functools.wraps(fn)
        async def wrapped(*args, **kwargs):
            session = async_session()
            try:
                res = await fn(session, *args, **kwargs)
            finally:
                await session.close()
            return res

        return wrapped

    return wrapper
