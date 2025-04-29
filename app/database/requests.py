from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import async_session, User, Item
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from typing import Tuple


async def get_user_id(tg_id: int):
    async with async_session() as session:
        stmt = select(User).where(User.tg_id == tg_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def add_user(tg_id: int, tg_name: str | None = None):
    async with async_session() as session:
        try:
            user = await get_user_id(tg_id)
            if user is None:
                new_user = User(tg_id=tg_id, tg_name=tg_name)
                session.add(new_user)
                await session.commit()
                return new_user
            return user
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Ошибка при добавлении пользователя: {e}")


async def get_items_by_category():
    async with async_session() as session:
        stmt = select(Item)
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_items(item_id):
    async with async_session() as session:
        items = await session.get(Item, item_id)
        return items


async def add_admin_id(tg_id: int, tg_name: str) -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        users = result.scalars().all()

        if users:
            user = users[0]
            user.admin_id = tg_id
        else:
            user = User(tg_id=tg_id, tg_name=tg_name, admin_id=tg_id)
            session.add(user)

        await session.commit()


async def is_admin(tg_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.admin_id == tg_id)
        )
        return result.scalar_one_or_none() is not None


async def delete_item(session: AsyncSession, item_id: int):
    print(f'удаление товара по id:{item_id}')
    await session.execute(delete(Item).where(Item.id == item_id))
    await session.commit()


class DBRequests:
    @staticmethod
    async def create_requests(session: AsyncSession, item_data: Tuple[str, str, int]):
        try:
            item_requests = Item(
                name=item_data[0],
                description=item_data[1],
                price=item_data[2]
            )

            session.add_all([item_requests])
            await session.commit()
            await session.refresh(item_requests)
            return item_requests

        except Exception as e:
            await session.rollback()
            print(f"Error creating requests: {e}")
            return None
