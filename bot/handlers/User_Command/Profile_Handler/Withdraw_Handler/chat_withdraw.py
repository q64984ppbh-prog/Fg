# main
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

# other
import re
import asyncio
from datetime import datetime
from data.config import db, client
from keyboards.User_Keyboards.Profile_Keyboards.Withdraw_Keyboards.withdraw_key import (
    start_withdraw_chat_keyboard,
    accept_withdraw_chat_keyboard,
    activated_check_user_keyboard
)

router = Router()

@router.message(F.text.regexp(r"^(выв(ести)?|вывод|vivod|vivid|vuvod)\s+(\d+(?:[.,]\d+)?\$*)$", flags=re.IGNORECASE))
async def deposit_message(message: Message):
    
    bot = message.bot
    chat_id = message.chat.id
    user_id = message.from_user.id
    message_id = message.message_id

    try:
        amount = float(re.sub(r"[^\d.,]", "", message.text).replace(",", "."))
    except ValueError:
        value_error_message = await bot.send_message(
            chat_id=chat_id,
            text="<b>❌ Укажите сумму вывода.\n\nПример: Вывод 1$</b>",
        )
        await asyncio.sleep(4)
        await bot.delete_message(chat_id=chat_id, message_id=value_error_message.message_id)
        return
    
    if await db.users.get_balance(user_id) >= amount:
        await bot.send_message(chat_id=chat_id,
                               text=f"<b>Сумма вывода — {amount}$\n\n👇 Выберите метод вывода</b>",
                               reply_markup=start_withdraw_chat_keyboard(user_id, amount),
                               reply_to_message_id=message_id)
    else:
        dell_message_error_balance = await bot.send_message(
            chat_id=chat_id,
            text=f"<b>❌ Недостаточно средств для вывода <code>{amount}$</code>.\n\nВаш баланс: <code>{await db.users.get_balance(user_id)}$</code></b>",
        )
        await asyncio.sleep(4)
        await bot.delete_message(chat_id=chat_id, message_id=dell_message_error_balance.message_id)

@router.callback_query(F.data.startswith("withdraw_chat_cryptobot_"))
async def call_withdraw_chat_cryptobot(call: CallbackQuery):

    chat_id = call.message.chat.id
    user_id = call.from_user.id 
    message_id = call.message.message_id

    data = call.data.split('_')
    withdraw_user_id = data[3]
    amount = data[4]
    
    if int(withdraw_user_id) != user_id:
        await call.answer("❌ Данное меню не ваше!", True)
        return 
    
    if await db.users.get_balance(user_id) < float(amount):
        await call.answer("❌ На балансе недостаточно средств", True)
        return 
    
    await call.answer()
    await call.bot.edit_message_text(chat_id=chat_id,
                                     message_id=message_id,
                                     text=f"<b>🌏 Crypto Bot — {amount} — USDT\n\n👇 Подтвердите вывод</b>",
                                     reply_markup=accept_withdraw_chat_keyboard(user_id, amount))
    
@router.callback_query(F.data.startswith("confirm_withdraw_cryptobot_"))
async def confirm_withdraw_chat_cryptobot(call: CallbackQuery):

    chat_id = call.message.chat.id
    user_id = call.from_user.id 
    username = call.from_user.username
    message_id = call.message.message_id

    data = call.data.split('_')
    withdraw_user_id = data[3]
    amount = data[4]
    
    if int(withdraw_user_id) != user_id:
        await call.answer("❌ Данное меню не ваше!", True)
        return 
    
    if await db.users.get_balance(user_id) < float(amount):
        await call.answer("❌ На балансе недостаточно средств", True)
        return 
    
    precent = float(amount) - (float(amount) * 0.03)
    now = datetime.now()
    formatted_time = now.strftime("%H:%M - %d.%m.%Y")

    try:
        check = await client.create_check(
            asset='USDT',
            amount=f"{precent:.2f}",
            pin_to_user_id=user_id
        )   

        await db.users.minus_balance(user_id, float(amount))
        await db.users.add_withdraw(user_id=user_id, amount=float(amount))
        await db.users.add_history_withdraw(user_id, float(amount), '🌏 Crypto Bot', formatted_time)

        url = check.bot_check_url
        await call.answer()
        await call.bot.edit_message_text(chat_id=chat_id,
                                         message_id=message_id,
                                         text=f"<b>🧾 Чек на {amount}$ для @{username}</b>",
                                         reply_markup=activated_check_user_keyboard(url, amount))
    except:
        pass

@router.callback_query(F.data.startswith("confirm_withdraw_cryptobot_"))
async def confirm_withdraw_chat_cryptobot(call: CallbackQuery):

    chat_id = call.message.chat.id
    user_id = call.from_user.id 
    username = call.from_user.username
    message_id = call.message.message_id

    data = call.data.split('_')
    withdraw_user_id = data[3]
    amount = data[4]
    
    if int(withdraw_user_id) != user_id:
        await call.answer("❌ Данное меню не ваше!", True)
        return 
    
    if await db.users.get_balance(user_id) < float(amount):
        await call.answer("❌ На балансе недостаточно средств", True)
        return 
    
    precent = float(amount) - (float(amount) * 0.03)
    now = datetime.now()
    formatted_time = now.strftime("%H:%M - %d.%m.%Y")

    try:
        check = await client.create_check(
            asset='USDT',
            amount=f"{precent:.2f}",
            pin_to_user_id=user_id
        )   

        await db.users.minus_balance(user_id, float(amount))
        await db.users.add_withdraw(user_id=user_id, amount=float(amount))
        await db.users.add_history_withdraw(user_id, float(amount), '🌏 Crypto Bot', formatted_time)

        # <!-- АДМИН СТАТИСТИКА --!>
        await db.admin.plus_admin_statistick('Amount_Replenishment', amount)
        await db.admin.plus_admin_statistick('Amount_Replenishment_Day', amount)

        url = check.bot_check_url
        await call.answer()
        await call.bot.edit_message_text(chat_id=chat_id,
                                         message_id=message_id,
                                         text=f"<b>🧾 Чек на {amount}$ для @{username}</b>",
                                         reply_markup=activated_check_user_keyboard(url, amount))
    except:
        pass


@router.callback_query(F.data.startswith("cancel_withdraw_cryptobot_"))
async def confirm_withdraw_chat_cryptobot(call: CallbackQuery):

    chat_id = call.message.chat.id
    user_id = call.from_user.id 
    message_id = call.message.message_id

    data = call.data.split('_')
    withdraw_user_id = data[3]
    
    if int(withdraw_user_id) != user_id:
        await call.answer("❌ Данное меню не ваше!", True)
        return 
    
    await call.answer()
    await call.bot.delete_message(chat_id=chat_id, message_id=message_id)


@router.callback_query(F.data.startswith("change_method_"))
async def change_method_chat(call: CallbackQuery):

    chat_id = call.message.chat.id
    user_id = call.from_user.id 
    message_id = call.message.message_id

    data = call.data.split('_')
    withdraw_user_id = data[2]
    amount = data[3]
    
    if int(withdraw_user_id) != user_id:
        await call.answer("❌ Данное меню не ваше!", True)
        return 
    
    await call.answer()
    await call.bot.edit_message_text(chat_id=chat_id,
                                     message_id=message_id,
                                     text=f"<b>Сумма вывода — {amount}$\n\n👇 Выберите метод вывода</b>",
                                    reply_markup=start_withdraw_chat_keyboard(user_id, amount))