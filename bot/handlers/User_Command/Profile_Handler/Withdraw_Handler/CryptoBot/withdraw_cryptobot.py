import uuid
from datetime import datetime
from aiogram import F, Router
from decimal import Decimal, InvalidOperation
from aiogram.types import CallbackQuery, Message, FSInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

from data.config import db, client
from utils.help_function import clean
from utils.decorators import require_subscription
from utils.logs_message import logs_succes_withdraw
from keyboards.User_Keyboards.Profile_Keyboards.Withdraw_Keyboards.withdraw_key import (
    back_in_withdraw_keyboard,
    accept_withdraw_keyboard,
    activated_check_user_keyboard
)

router = Router()

class WithdrawState(StatesGroup):
    waiting_amount = State()

@router.callback_query(F.data == 'start_withdraw_cryptobot')
@require_subscription()
async def call_start_withdraw_cryptobot(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    balance = await db.users.get_balance(user_id)
    min_withdraw = float(await db.admin.get_value("Min_Withdraw") or 0.5)

    if balance < min_withdraw:
        await call.answer(f"❌ Минимальный вывод от {min_withdraw:.2f}$", show_alert=True)
        return

    await state.clear()
    await state.set_state(WithdrawState.waiting_amount)

    await call.answer()
    await call.message.delete()
    await call.bot.send_message(
        chat_id=user_id,
        caption=clean(f"""💡 Выбрана система: <b>🌏 Crypto Bot</b>

💰 Ваш баланс: <b>{balance:.2f}$</b>

ℹ️ Введите сумму для вывода:"""),
        reply_markup=back_in_withdraw_keyboard()
    )

@router.message(WithdrawState.waiting_amount)
async def withdraw_amount_input(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    # Убираем $ и запятые
    raw = message.text.strip().replace('$', '').replace(',', '.').replace(' ', '')
    
    try:
        amount = Decimal(raw)
    except InvalidOperation:
        await message.answer("<b>❌ ОШИБКА!</b>\n<blockquote>Введите корректную сумму</blockquote>")
        return

    if amount <= 0:
        await message.answer("<b>❌ ОШИБКА!</b>\n<blockquote>Сумма должна быть больше 0</blockquote>")
        return

    balance = Decimal(str(await db.users.get_balance(user_id)))
    min_withdraw = Decimal(str(await db.admin.get_value("Min_Withdraw") or 0.5))
    max_withdraw = balance

    if amount < min_withdraw:
        await message.answer(f"<b>❌ ОШИБКА!</b>\n<blockquote>Минимальный вывод: {min_withdraw:.2f}$</blockquote>")
        return

    if amount > max_withdraw:
        await message.answer(f"<b>❌ ОШИБКА!</b>\n<blockquote>Недостаточно средств\nВаш баланс: {balance:.2f}$</blockquote>")
        return

    await state.clear()

    # Списываем баланс
    if not await db.users.try_reserve_balance(user_id, amount):
        await message.answer("<b>❌ ОШИБКА!</b>\n<blockquote>Не удалось зарезервировать средства</blockquote>")
        return

    now = datetime.now()
    await db.users.add_withdraw(user_id, amount)
    await db.users.add_history_withdraw(user_id, amount, '🌏 Crypto Bot', now)

    try:
        await db.admin.plus_admin_statistick('Amount_Replenishment', float(amount))
        await db.admin.plus_admin_statistick('Amount_Replenishment_Day', float(amount))
    except:
        pass

    await db.send.add_out_to_check(float(amount), user_id, username)

    new_balance = await db.users.get_balance(user_id)

    photo = FSInputFile('photo/profile.jpg')
    await message.answer_photo(
        photo=photo,
        caption=clean(f"""<b>💸 Вывод успешен!</b>

<blockquote><b>✅ Ваш чек на сумму <code>{amount:.2f}$</code> успешно добавлен к выводу.</b></blockquote>

<b>ℹ️ Ожидайте чек от бота</b>"""),
        reply_markup=back_in_withdraw_keyboard()
    )

    try:
        check = await client.create_check(asset='USDT', amount=str(amount))
        await message.answer(
            caption=f"<b>🚀 Получить {amount:.2f}$ от DuckWIN</b>",
            reply_markup=activated_check_user_keyboard(check.bot_check_url, float(amount)),
            disable_web_page_preview=False
        )
        await logs_succes_withdraw(username, first_name, user_id, float(amount), new_balance, message.bot)
    except Exception as e:
        print(f"Ошибка создания чека: {e}")
        await db.users.add_balance(user_id, float(amount))
        await message.answer(clean("""<i>❌ Произошла ошибка.</i>
                              
• <code>Ошибка с нашей стороны</code>
• <code>USDT зачислены обратно</code>
• <code>Попробуйте чуть позже</code>"""))
