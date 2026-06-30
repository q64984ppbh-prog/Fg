# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

# other
import asyncio
from data.config import db
from datetime import datetime
from utils.help_function import clean
from utils.logs_message import logs_succes_deposit
import handlers.User_Command.Profile_Handler.Deposit_Handler.function as functions
from keyboards.User_Keyboards.Profile_Keyboards.Deposit_Keyboards.deposit_key import (
    back_in_deposit_keyboard,
    deposit_message_keyboard
)

router = Router()
class DepositCryptoBotState(StatesGroup):

    amount = State()

@router.callback_query(F.data == 'start_dep_cryptobot')
async def call_dep_cryptobot(call: CallbackQuery, state: FSMContext):

    bot = call.bot
    user_id = call.from_user.id 
    message_id = call.message.message_id 

    await call.answer()
    await bot.edit_message_text(chat_id=user_id,
                                   message_id=message_id,
                                   caption=clean(f"""
                                    💡 Выбрана система: <b>🌏 Crypto Bot</b>

                                    <blockquote><b>🌏 Crypto Bot</b> — предназначен для хранения, отправки и покупки криптовалют прямо внутри Telegram.</blockquote>
                                                 
                                    🦋 Введите <b>сумму ($)</b> для оплаты:"""),
                                    reply_markup=back_in_deposit_keyboard())
    await state.set_state(DepositCryptoBotState.amount)

@router.message(StateFilter(DepositCryptoBotState.amount))
async def message_deposit_cryptobot(message: Message, state: FSMContext):

    bot = message.bot
    user_id = message.from_user.id 
    username = message.from_user.username
    first_name = message.from_user.first_name
    message_id = message.message_id

    try:
        amount = float(message.text)
    except:
        photo = FSInputFile('photo/profile.jpg')
        await bot.send_message(chat_id=user_id,
                             caption=clean(f"""
                            <code>[ERR]</code> <b>❌ Бот заметил ошибку!</b>
                                           
                            💸 Отправьте <b>верную сумму</b> для пополнения:"""),
                            reply_markup=back_in_deposit_keyboard())
        return
    
    min_dep = await db.admin.get_value('Min_Dep')
    max_dep = await db.admin.get_value('Max_Dep')

    if amount >= min_dep and amount <= max_dep:
        
        amount_invoice = amount  - (amount * 0.03)
        #amount_invoice = amount
        invoice = await functions.create_invoice(amount, 'USDT')
        if invoice:
            url = invoice.bot_invoice_url
            invoice_id = invoice.invoice_id

            await state.clear()
            photo = FSInputFile('photo/profile.jpg')
            soo = await bot.send_message(chat_id=user_id,
                                 caption=clean(f"""
                                ✅ Счет на оплату <b>создан</b>
                                
                                <blockquote>📖 <b>Информация</b> счета
                                ├ <code>🔄 Проверка оплаты автомат.</code>
                                ├ Сумма: <b>{amount:.2f}$</b>
                                ├ Система: <a href='https://t.me/send'><b>🌏 Crypto Bot</b></a>
                                └ Время оплаты: <b>5 мин.</b></blockquote>
                                
                                <b>👤 Оплатите счет для пополнения баланса!</b>"""),
                                reply_markup=deposit_message_keyboard(url))
            
            if await asyncio.create_task(functions.check_date_proverka(invoice_id)):

                now = datetime.now()
                formatted_time = now.strftime("%H:%M - %d.%m.%Y")

                await db.users.add_balance(user_id=user_id, amount=float(amount_invoice))
                await db.users.add_history_replenishment(user_id=user_id, amount=float(amount), system="🌏 Crypto Bot", date=formatted_time)
                await db.users.add_replenishment(user_id=user_id, amount=amount)

                # <!-- АДМИН СТАТИСТИКА --!>
                await db.admin.plus_admin_statistick('Amount_Deposit', amount)

                await bot.delete_message(chat_id=user_id, message_id=soo.message_id)
                await bot.send_message(chat_id=user_id,
                                     caption=clean(f"""
                                    ✅ Счет <b>оплачен</b>!
                                    
                                    <blockquote>📖 <b>Информация</b> счета
                                    ├ <code>🔄 Проверка оплаты автомат.</code>
                                    ├ Сумма: <b>{amount:.2f}$</b>
                                    ├ Система: <a href='https://t.me/send'><b>🌏 Crypto Bot</b></a>
                                    └ Время оплаты: <b>5 мин.</b></blockquote>
                                    
                                    💰 На ваш <b>баланс</b> зачислено <b>{amount_invoice}$</b>"""),
                                    message_effect_id="5104841245755180586",
                                    reply_markup=back_in_deposit_keyboard())
                await logs_succes_deposit(username, first_name, user_id, amount, await db.users.get_balance(user_id), bot)

            else:
                await bot.delete_message(chat_id=user_id, message_id=soo.message_id)

        else:
            photo = FSInputFile('photo/profile.jpg')
            await bot.send_message(chat_id=user_id,
                             caption=clean(f"""
                            <code>[ERR]</code> <b>❌ Бот заметил ошибку!</b>
                                           
                            👨🏻‍💻 Произошла <b>Тех.Ошибка</b>, обратитесь в поддержку"""),
                            reply_markup=back_in_deposit_keyboard())
    else:
        photo = FSInputFile('photo/profile.jpg')
        await bot.send_message(chat_id=user_id,
                             caption=clean(f"""
                            <code>[ERR]</code> <b>❌ Бот заметил ошибку!</b>
                                           
                            💸 Диапозон от <b>{min_dep:.2f}$</b> до <b>{max_dep:.0f}$</b>"""),
                            reply_markup=back_in_deposit_keyboard())