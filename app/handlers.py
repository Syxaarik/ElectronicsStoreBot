from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, SuccessfulPayment

from app.database.requests import add_user, get_items
import app.keyboards as kb
import os

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
        await callback.message.answer(text, parse_mode='HTML', reply_markup=await kb.pay_or_back(item.id))
    else:
        await callback.message.answer("Товар не найден.")


@router.callback_query(F.data.startswith('pay_'))
async def command_pay(message: Message, bot: Bot, callback: CallbackQuery):
    item = await get_items(int(callback.data.split('_')[1]))
    try:
        await bot.send_invoice(
            chat_id=message.chat.id,
            title=item.name,
            description=item.description,
            payload=str(item.id),  # Уникальный идентификатор платежа
            provider_token='1744374395:TEST:0b2dbdcab951620502a6',  # Токен от BotFather
            currency="RUB",  # Валюта (RUB, USD, EUR и т.д.)
            prices=[LabeledPrice(label=item.name, amount=int(item.price * 100))],
            start_parameter="create_invoice_test",
            provider_data=None,
            photo_url=None,
            photo_size=None,
            photo_width=None,
            photo_height=None,
            need_name=True,
            need_phone_number=True,
            need_email=True,
            need_shipping_address=False,
            send_phone_number_to_provider=False,
            send_email_to_provider=False,
            is_flexible=False,
            disable_notification=False,
            protect_content=False,
            reply_to_message_id=None,
            allow_sending_without_reply=True,
            reply_markup=None,
            request_timeout=15
        )
    except Exception as e:
        print(f"Ошибка: {e}")


@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message(lambda message: message.successful_payment is not None)
async def successful_payment(message: Message):
    await message.answer("Платеж успешно завершен! Спасибо за покупку!")
