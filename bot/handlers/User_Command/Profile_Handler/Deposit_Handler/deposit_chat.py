# main
from aiogram import F, Router
from aiogram.types import Message

# other
import re
import asyncio
from datetime import datetime
from utils.help_function import clean
from utils.logs_message import logs_succes_deposit
from data.config import db, name_casino, username_bot_casino
import handlers.User_Command.Profile_Handler.Deposit_Handler.function as functions
from keyboards.User_Keyboards.Profile_Keyboards.Deposit_Keyboards.deposit_key import (
    deposit_message_keyboard
)


router = Router()

@router.message(F.text.regexp(r"^(деп(нуть)?|депозит|dep(osit|nyt)?)\s+(\d+(?:[.,]\d+)?\$*)$", flags=re.IGNORECASE))
async def deposit_message(message: Message):
    
    bot = message.bot
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name


    try:
        amount = float(re.sub(r"[^\d.,]", "", message.text).replace(",", "."))
    except ValueError:
        error_soo_value_error = await bot.send_message(
            chat_id=chat_id,
            caption="<blockquote>❌ Неверный формат суммы. Пример: <code>деп 10</code> или <code>deposit 0.5$</code></blockquote>",
        )
        await asyncio.sleep(4)
        await bot.delete_message(chat_id=chat_id, message_id=error_soo_value_error .message_id)
        return

    soo = await bot.send_message(
        chat_id=chat_id,
        caption="<b>⌛️ Создание счёта для пополнения...</b>",
    )

    amount_invoice = amount - (amount * 0.03)
    min_dep = await db.admin.get_value("Min_Dep")
    max_dep = await db.admin.get_value("Max_Dep")

    if min_dep <= amount <= max_dep:
        invoice = await functions.create_invoice(amount, "USDT")
        if not invoice:
            error_message = await bot.edit_message_text(
                chat_id=chat_id,
                message_id=soo.message_id,
                caption="<b>❌ Ошибка при создании счёта. Попробуйте позже.</b>",
            )
            await asyncio.sleep(4)
            await bot.delete_message(chat_id=chat_id, message_id=error_message.message_id)
            return

        url = invoice.bot_invoice_url
        invoice_id = invoice.invoice_id
        user_display = f"@{username}" if username else f"ID: {user_id}"

        mess = await bot.edit_message_text(
            chat_id=chat_id,
            message_id=soo.message_id,
            caption=clean(f"""
            <b>🎁 Счёт для пополнения создан!</b>

            <blockquote>👤 Будьте внимательны — счёт создан для <b>{user_display}</b></blockquote>

            <b>ℹ️ Нажмите, чтобы пополнить баланс на {amount}$</b>
            """),
            reply_markup=deposit_message_keyboard(url),
        )

        if await asyncio.create_task(functions.check_date_proverka(invoice_id)):

            now = datetime.now()
            formatted_time = now.strftime("%H:%M - %d.%m.%Y")

            await db.users.add_balance(user_id=user_id, amount=float(amount_invoice))
            await db.users.add_history_replenishment(user_id=user_id, amount=float(amount), system="🌏 Crypto Bot", date=formatted_time)
            await db.users.add_replenishment(user_id=user_id, amount=amount)

            # <!-- АДМИН СТАТИСТИКА --!>
            await db.admin.plus_admin_statistick('Amount_Deposit', amount)

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=mess.message_id,
                caption=f"<b>✅ Баланс @{username} пополнен на {amount}$</b>",
            )
            await logs_succes_deposit(
                username, first_name, user_id, amount, await db.users.get_balance(user_id), bot
            )
        else:
            await bot.delete_message(chat_id=chat_id, message_id=mess.message_id)

    else:
        await asyncio.sleep(0.3)
        delmess = await bot.edit_message_text(
            chat_id=chat_id,
            message_id=soo.message_id,
            caption=clean(f"""
            <b><a href='https://t.me/{username_bot_casino}'>🤖 {name_casino} Bot</a> заметил ошибку!</b>

            <blockquote><i>✍🏻 Вы <b>ввели неправильный</b> диапазон!</i></blockquote>
            
            ℹ️ Диапазон: <b>{min_dep:.2f}$</b> - <b>{max_dep:.0f}$</b>
            """),
        )
        await asyncio.sleep(4)
        await bot.delete_message(chat_id=chat_id, message_id=delmess.message_id)