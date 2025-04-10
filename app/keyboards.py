from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_item

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Каталог🛒', callback_data='catalog')],
        [InlineKeyboardButton(text='Контакты☎', callback_data='contact')]
    ]
)


async def set_item():
    all_item = await get_item()
    keyboard = InlineKeyboardBuilder()

    for items in all_item:
        keyboard.row(InlineKeyboardButton(text=items.name, callback_data='_item'))
    keyboard.row(InlineKeyboardButton(text='<-Назад', callback_data='catalog'))
