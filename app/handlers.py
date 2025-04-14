from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from app.database.requests import add_user, get_items
import app.keyboards as kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    tg_id = message.from_user.id
    tg_name = message.from_user.full_name

    await add_user(tg_id=tg_id, tg_name=tg_name)
    await message.answer(f'Привет мой друг {message.from_user.full_name}', reply_markup=kb.main)


@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.message.edit_text('Выберите товар', reply_markup=await kb.keyboard_item())


@router.callback_query(F.data.startswith('item_'))
async def show_item(callback: CallbackQuery):
    item_id = int(callback.data.split('_')[1])
    item = await get_items(item_id)

    if item:
        text = f"<b>{item.name}:</b>\n\n{item.description}\n💰 Цена: {item.price}₽"
        await callback.message.edit_text(text, parse_mode='HTML', reply_markup=kb.back_in_catalog)
    else:
        await callback.message.answer("Товар не найден.")
