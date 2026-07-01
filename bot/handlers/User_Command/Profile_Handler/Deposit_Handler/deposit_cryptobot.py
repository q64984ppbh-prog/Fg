from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from data.config import db, client
from utils.help_function import clean
from utils.decorators import require_subscription
from keyboards.User_Keyboards.Profile_Keyboards.Deposit_Keyboards.deposit_key import back_in_deposit_keyboard
import handlers.User_Command.Profile_Handler.Deposit_Handler.function as functions

router = Router()

class DepositState(StatesGroup):
    waiting_amount = State()

@router.callback_query(F.data == 'start_deposit_cryptobot')
@require_subscription()
async def call_dep_cryptobot(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    balance = await db.users.get_balance(user_id)
    await state.clear()
    await state.set_state(DepositState.waiting_amount)
    await call.answer()
    await call.message.delete()
    await call.bot.send_message(
        chat_id=user_id,
        text=clean(f"💡 Выбрана система: <b>🌏 Crypto Bot</b>\n\n💰 Ваш баланс: <b>{balance:.2f}$</b>\n\nℹ️ Введите сумму для пополнения:"),
        reply_markup=back_in_deposit_keyboard()
    )

@router.message(DepositState.waiting_amount)
async def deposit_amount_input(message: Message, state: FSMContext):
    user_id = message.from_user.id
    raw = message.text.strip().replace('$', '').replace(',', '.').replace(' ', '')
    try:
        amount = float(raw)
    except ValueError:
        await message.answer("<b>❌ ОШИБКА!</b>\n<blockquote>Введите корректную сумму</blockquote>")
        return
    if amount <= 0:
        await message.answer("<b>❌ ОШИБКА!</b>\n<blockquote>Сумма должна быть больше 0</blockquote>")
        return
    min_dep = float(await db.admin.get_value("Min_Dep") or 0.2)
    max_dep = float(await db.admin.get_value("Max_Dep") or 10000)
    if amount < min_dep:
        await message.answer(f"<b>❌ ОШИБКА!</b>\n<blockquote>Минимальный депозит: {min_dep:.2f}$</blockquote>")
        return
    if amount > max_dep:
        await message.answer(f"<b>❌ ОШИБКА!</b>\n<blockquote>Максимальный депозит: {max_dep:.2f}$</blockquote>")
        return
    await state.clear()
    invoice = await functions.create_invoice(amount, 'USDT')
    if invoice:
        await message.answer(
            f"<b>🧾 Счёт на {amount}$ создан!</b>\n\n"
            f"<a href='{invoice.bot_invoice_url}'>Оплатить через CryptoBot</a>",
            disable_web_page_preview=True
        )
    else:
        await message.answer("<b>❌ Ошибка при создании счёта. Попробуйте позже.</b>")
