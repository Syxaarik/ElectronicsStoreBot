from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from app.database.requests import add_user, get_items
import app.keyboards as kb
import os

router = Router()
load_dotenv()


class Form(StatesGroup):
    admin_key = State()


@router.message(CommandStart())
async def start(message: Message):
    await add_user(tg_id=message.from_user.id, tg_name=message.from_user.full_name)
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
        await callback.message.answer(text, parse_mode='HTML', reply_markup=await kb.pay_or_back(item.id))
    else:
        await callback.message.answer("Товар не найден.")


@router.callback_query(F.data.startswith('pay_'))
async def command_pay(callback: CallbackQuery, bot):
    item = await get_items(int(callback.data.split('_')[1]))
    PRICE = [types.LabeledPrice(label=item.name, amount=int(item.price * 100))]
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Тестовый товар",
        description="Описание",
        payload="payload-test",
        provider_token=os.getenv('PAY_TOKEN'),
        currency="RUB",
        prices=PRICE,
        start_parameter="start-param",
    )
    await callback.answer()


# Сделать обработку на ключ админа, что бы его можно было вписать и FSM
@router.callback_query(F.data == 'admin_reg')
async def admin_set(message: Message, state: FSMContext):
    await state.set_state(Form.admin_key)
    await message.answer('Введите ключ для входа в админ панель:')


@router.message(Form.admin_key)
async def admin(message: Message, state: FSMContext):
    await state.update_data(key=message.text)
    data = await state.get_data()
    key = '1234'

    # Добавление проверки на ID для admin и создание кнопак редактирования
    if data['key'] == key:
        await message.answer('Вы попали в админ панель.')
       # await add_admin(tg_id=message.from_user.id)
        await state.clear()
    else:
        await message.answer(f'Не верный ключ. \nПравильный ключ был: {data['key']}')
        await state.clear()
