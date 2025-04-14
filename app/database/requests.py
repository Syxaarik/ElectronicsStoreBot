from app.database.models import async_session, User, Item
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError


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
