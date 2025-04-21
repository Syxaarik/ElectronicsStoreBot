from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_items_by_category

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Каталог🛒', callback_data='catalog'),
         InlineKeyboardButton(text='Контакты☎', callback_data='contact')],
        [InlineKeyboardButton(text='Админ-панель♿', callback_data='admin_reg')]
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
    keyboard.row(InlineKeyboardButton(text='Оплатить💲', callback_data=f'pay_{item_id}'))
    keyboard.row(InlineKeyboardButton(text='К каталогу⬅', callback_data='catalog'))
    return keyboard.as_markup()


admin_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Создание товара🛠', callback_data="create_item"),
         InlineKeyboardButton(text='Удаление товара🗑', callback_data='delete_item')],
        [InlineKeyboardButton(text='К каталогу⬅', callback_data='catalog')]
    ]
)
