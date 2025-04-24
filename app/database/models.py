import os

from dotenv import load_dotenv
from sqlalchemy import BigInteger, String
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

load_dotenv()

engine = create_async_engine(url=os.getenv('DB'))
async_session = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped['int'] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped['int'] = mapped_column(BigInteger, unique=True)
    tg_name: Mapped['str'] = mapped_column(String, nullable=True)
    admin_id: Mapped['int'] = mapped_column(BigInteger, nullable=False, default=0)


class Item(Base):
    __tablename__ = 'items'

    id: Mapped['int'] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped['str'] = mapped_column(String(25))
    description: Mapped['str'] = mapped_column(String(512))
    price: Mapped['int']


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
