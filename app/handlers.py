from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from typing import AsyncIterator
from dotenv import load_dotenv

from app.database.requests import add_user, get_items, add_admin_id, is_admin, delete_item, DBRequests
from app.database.models import get_db_session
import app.keyboards as kb
import os

router = Router()
load_dotenv()


class Form(StatesGroup):
    admin_key = State()
    item_name = State()
    item_description = State()
    item_price = State()


@router.message(CommandStart())
async def start(message: Message):
    await add_user(tg_id=message.from_user.id, tg_name=message.from_user.full_name)
    await message.answer(f'Привет мой друг {message.from_user.full_name}', reply_markup=kb.main)


@router.callback_query(F.data == 'contact')
async def contact(callback: CallbackQuery):
    await callback.message.answer('За помощью обращайтесь @Sheff_Shen')


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
        title=item.name,
        description=item.description,
        payload="payload-test",
        provider_token=os.getenv('PAY_TOKEN'),
        currency="RUB",
        prices=PRICE,
        start_parameter="start-param",
    )
    await callback.answer()


@router.callback_query(F.data == 'admin_reg')
async def admin_set(callback: CallbackQuery, state: FSMContext):
    if await is_admin(callback.from_user.id):
        await callback.message.answer("✅ Вы уже админ. Добро пожаловать в панель!", reply_markup=kb.admin_keyb)
        return

    await state.set_state(Form.admin_key)
    await callback.message.answer('Введите ключ для входа в админ панель:')
    await callback.answer()


@router.message(Form.admin_key)
async def admin(message: Message, state: FSMContext):
    await state.update_data(key=message.text)
    data = await state.get_data()

    # Добавление проверки на ID для admin и создание кнопок редактирования
    if data['key'] == '1999':
        await state.clear()
        await add_admin_id(message.from_user.id, message.from_user.full_name)
        await message.answer(f'Вы попали в админ панель.', reply_markup=kb.admin_keyb)
    else:
        await message.answer(f'Не верный ключ.')
        await state.clear()


@router.callback_query(F.data == 'create_item')
async def get_item_create(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.item_name)
    await callback.message.answer('Введите название предмета:')
    await callback.answer()


@router.message(Form.item_name)
async def get_item_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.item_description)
    await message.answer('Введите описание предмета:')


@router.message(Form.item_description)
async def get_item_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Form.item_price)
    await message.answer('Введите цену предмета:')


@router.message(Form.item_price)
async def add_item(message: types.Message, state: FSMContext):
    try:
        await state.update_data(price=message.text)
        data = await state.get_data()
        item_data = (data['name'], data['description'], int(data['price']))
        await message.answer(f"Товар создан!\nНазвание: {data['name']}"
                             f"\nОписание: {data['description']}"
                             f"\nЦена: {data['price']}₽")

        session_generator: AsyncIterator = get_db_session()
        db_session = await anext(session_generator)

        await DBRequests.create_requests(
            db_session,
            item_data,
        )

        await state.clear()
    except ValueError:
        await message.answer('Пожалуйста, введите корректную цену (только число)')


@router.callback_query(F.data == 'delete_item')
async def get_item_delete(callback: CallbackQuery):
    await callback.message.edit_text('Выбери предмет для удаления:', reply_markup=await kb.delete_item_keyb())


@router.callback_query(F.data.startswith('delete_'))
async def delete_item(callback: CallbackQuery, session):
    item_id = int(callback.data.split('_')[1])
    await delete_item(session, item_id)
    await callback.message.edit_text('Товар удален\n Выберите кнопку из меню', reply_markup=kb.main)
