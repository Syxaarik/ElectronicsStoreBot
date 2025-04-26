from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import async_session

class DBSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with async_session() as session:
            data["session"] = session
            return await handler(event, data)