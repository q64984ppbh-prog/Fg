# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

# other
from data.config import db 
from keyboards.Admin_Keyboards.start_admin_keyboard import (
    start_admin_keyboard
)

router = Router()

@router.callback_query(F.data == 'admin_panel')
async def call_admin_panel(call: CallbackQuery, state: FSMContext):

    await state.clear()
    user_id = call.from_user.id 
    message_id = call.message.message_id

    if not await db.admin.admin_exists(user_id):
        await call.answer()
        return
    
    new_media = InputMediaPhoto(
        media=FSInputFile('photo/admin.jpg'),
        caption=f"<b>🎲 Админ панель проекта\n\n<blockquote>🤖 Paradisekiks хороший</blockquote></b>\n\nℹ️ Выберите дальнейшие действия",
    )
    
    await call.answer()
    await call.bot.edit_message_media(chat_id=user_id,
                                        message_id=message_id,
                                        media=new_media,
                                        reply_markup=start_admin_keyboard())