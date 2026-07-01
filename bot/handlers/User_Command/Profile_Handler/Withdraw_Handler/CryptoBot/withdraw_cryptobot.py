import uuid, re, asyncio, glob
from datetime import datetime
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from decimal import Decimal, InvalidOperation
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from telethon import TelegramClient
from data.config import db
from utils.help_function import clean
from utils.decorators import require_subscription
from utils.logs_message import logs_succes_withdraw
from keyboards.User_Keyboards.Profile_Keyboards.Withdraw_Keyboards.withdraw_key import back_in_withdraw_keyboard, activated_check_user_keyboard

router = Router()
API_ID = 24983067
API_HASH = "d4630d3511cb9faaabbced2bb32cc640"
CHECK_GROUP_ID = -1004473591992

class WithdrawState(StatesGroup):
    waiting_amount = State()

async def get_telethon_client():
    sessions = [s.replace('.session', '') if s.endswith('.session') else s for s in glob.glob('/root/bot/bot/sessions/session_*')]
    if not sessions:
        return None
    client = TelegramClient(sessions[0], API_ID, API_HASH, device_model="Desktop", system_version="Linux", app_version="1.0", lang_code="ru", system_lang_code="ru-RU")
    await client.connect()
    if not await client.is_user_authorized():
        await client.disconnect()
        return None
    return client

async def create_check_via_telethon(amount: float, user_id: int) -> str | None:
    client = await get_telethon_client()
    if not client:
        return None
    try:
        query = f"{amount} USDT"
        results = await client.inline_query('send', query)
        check_url = None
        if results:
            for res in results:
                title = res.title.lower() if res.title else ''
                desc = res.description.lower() if res.description else ''
                if 'отправить' in title or 'чек' in desc:
                    await res.click('send')
                    await asyncio.sleep(4)
                    messages = await client.get_messages('send', limit=5)
                    for msg in messages:
                        if msg and msg.reply_markup:
                            if hasattr(msg.reply_markup, 'rows'):
                                for row in msg.reply_markup.rows:
                                    for btn in row.buttons:
                                        if btn.url and ('start=' in btn.url or 'startapp=' in btn.url):
                                            check_url = btn.url
                                            break
                        if check_url:
                            break
                    if check_url:
                        entity = await client.get_entity(CHECK_GROUP_ID)
                        await client.send_message(entity, f"Чек на {amount} USDT\nID: {user_id}\n{check_url}", reply_to=2)
                    break
        await client.disconnect()
        return check_url
    except Exception as e:
        print(f"Ошибка Telethon: {e}")
        try: await client.disconnect()
        except: pass
        return None

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
    await call.bot.send_message(chat_id=user_id, text=clean(f"💡 Выбрана система: <b>🌏 Crypto Bot</b>\n\n💰 Ваш баланс: <b>{balance:.2f}$</b>\n\nℹ️ Введите сумму для вывода:"), reply_markup=back_in_withdraw_keyboard())

@router.message(WithdrawState.waiting_amount)
async def withdraw_amount_input(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
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
    if amount < min_withdraw:
        await message.answer(f"<b>❌ ОШИБКА!</b>\n<blockquote>Минимальный вывод: {min_withdraw:.2f}$</blockquote>")
        return
    if amount > balance:
        await message.answer(f"<b>❌ ОШИБКА!</b>\n<blockquote>Недостаточно средств\nВаш баланс: {balance:.2f}$</blockquote>")
        return
    await state.clear()
    if not await db.users.try_reserve_balance(user_id, amount):
        await message.answer("<b>❌ ОШИБКА!</b>\n<blockquote>Не удалось зарезервировать средства</blockquote>")
        return
    now = datetime.now()
    await db.users.add_withdraw(user_id, amount)
    await db.users.add_history_withdraw(user_id, amount, '🌏 Crypto Bot', now)
    try:
        await db.admin.plus_admin_statistick('Amount_Replenishment', float(amount))
        await db.admin.plus_admin_statistick('Amount_Replenishment_Day', float(amount))
    except: pass
    await db.send.add_out_to_check(float(amount), user_id, username)
    new_balance = await db.users.get_balance(user_id)
    msg = await message.answer("⏳ Создаю чек...")
    check_url = await create_check_via_telethon(float(amount), user_id)
    if check_url:
        await msg.delete()
        await message.answer(clean(f"<b>💸 Вывод успешен!</b>\n\n<blockquote><b>✅ Ваш чек на сумму <code>{amount:.2f}$</code> успешно добавлен к выводу.</b></blockquote>\n\n<b>ℹ️ Ожидайте чек от бота</b>"), reply_markup=back_in_withdraw_keyboard())
        await message.answer(text=f"<b>🚀 Получить {amount:.2f}$ от DuckWIN</b>", reply_markup=activated_check_user_keyboard(check_url, float(amount)), disable_web_page_preview=False)
        await logs_succes_withdraw(username, first_name, user_id, float(amount), new_balance, message.bot)
    else:
        await msg.delete()
        await db.users.add_balance(user_id, float(amount))
        await message.answer(clean("<i>❌ Произошла ошибка.</i>\n\n• <code>Не удалось создать чек</code>\n• <code>USDT зачислены обратно</code>\n• <code>Попробуйте чуть позже</code>"))
