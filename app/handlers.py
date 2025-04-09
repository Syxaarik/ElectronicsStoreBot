from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database.requests import add_user

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    tg_id = message.from_user.id
    tg_name = message.from_user.full_name

    await add_user(tg_id=tg_id, tg_name=tg_name)
    await message.answer(f'Привет мой друг {message.from_user.full_name}')
