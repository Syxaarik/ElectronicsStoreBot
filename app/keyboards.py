from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_items_by_category

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Каталог🛒', callback_data='catalog')],
        [InlineKeyboardButton(text='Контакты☎', callback_data='contact')]
    ]
)


async def keyboard_item():
    all_items = await get_items_by_category()
    keyboard = InlineKeyboardBuilder()

    for item in all_items:
        keyboard.row(InlineKeyboardButton(text=item.name, callback_data=f'item_{item.id}'))
    return keyboard.as_markup()


async def pay_or_back(item_id: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='💲Оплатить💲', callback_data=f'item_{item_id}'))
    keyboard.row(InlineKeyboardButton(text='К каталогу⬅', callback_data='catalog'))
    return keyboard.as_markup()
