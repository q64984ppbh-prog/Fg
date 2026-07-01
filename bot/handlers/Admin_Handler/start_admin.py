from aiogram import F, Router
from aiogram.types import CallbackQuery
from data.config import db
from utils.help_function import clean
from keyboards.Admin_Keyboards.start_admin_keyboard import start_admin_keyboard

router = Router()

@router.callback_query(F.data == 'admin_panel')
async def call_admin_panel(call: CallbackQuery):
    user_id = call.from_user.id
    await call.answer()
    await call.message.delete()
    await call.bot.send_message(
        user_id,
        text="<b>🎲 Админ панель проекта</b>\n\n<blockquote>🤖 Weskercode хороший</blockquote>\n\nℹ️ Выберите дальнейшие действия",
        parse_mode='HTML',
        reply_markup=start_admin_keyboard()
    )
