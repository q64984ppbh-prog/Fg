from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from data.config import db
from utils.help_function import clean

router = Router()

class MailingStates(StatesGroup):
    waiting_text = State()
    waiting_confirm = State()

@router.callback_query(F.data == 'mailing_project')
async def start_send_message(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.bot.send_message(
        chat_id=call.from_user.id,
        text="<b>📨 Введите текст для рассылки:</b>"
    )
    await state.set_state(MailingStates.waiting_text)

@router.message(MailingStates.waiting_text)
async def get_text_mailing(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(
        f"<b>📨 Текст рассылки:</b>\n\n{message.text}\n\n<b>Отправить?</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да", callback_data="confirm_mailing")],
            [InlineKeyboardButton(text="❌ Нет", callback_data="cancel_mailing")]
        ])
    )
    await state.set_state(MailingStates.waiting_confirm)

@router.callback_query(F.data == 'confirm_mailing', MailingStates.waiting_confirm)
async def send_mailing(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data['text']
    users = await db.users.get_all_users()
    count = 0
    for user in users:
        try:
            await call.bot.send_message(user['user_id'], text)
            count += 1
        except:
            pass
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, f"✅ Рассылка отправлена {count} пользователям.")
    await state.clear()

@router.callback_query(F.data == 'cancel_mailing', MailingStates.waiting_confirm)
async def cancel_mailing(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.bot.send_message(call.from_user.id, "❌ Рассылка отменена.")
    await state.clear()
