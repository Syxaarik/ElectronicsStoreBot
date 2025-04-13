from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_all_items

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Каталог🛒', callback_data='catalog')],
        [InlineKeyboardButton(text='Контакты☎', callback_data='contact')]
    ]
)


async def keyboard_item():
    all_item = await get_all_items()
    keyboard = InlineKeyboardBuilder()

    for item in all_item:
        keyboard.row(InlineKeyboardButton(text=item.name, callback_data=f'item_{item.id}'))
    return keyboard.as_markup()
