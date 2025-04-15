import asyncio
import logging
import os
import sys

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import router
from app.database.models import init_db


async def main():
    load_dotenv()
    await init_db()
    dp = Dispatcher(router=router)
    dp.include_router(router)
    bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())
