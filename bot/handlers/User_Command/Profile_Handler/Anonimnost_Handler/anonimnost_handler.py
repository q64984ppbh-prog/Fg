# main
from aiogram import F, Router
from aiogram.types import CallbackQuery

# other
from data.config import db
from keyboards.User_Keyboards.Profile_Keyboards.profile_keyboard import start_profile_keyboard

router = Router()

@router.callback_query(F.data == 'private_user')
async def call_private_user(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    if await db.users.get_anonimnost(user_id):
        await db.users.update_anonimnost(user_id, False)
        await call.answer(text="👤 Вы выключили анонимность! Теперь ваш ник виден!", show_alert=True)
    else:
        await db.users.update_anonimnost(user_id, True)
        await call.answer(text="🥷🏻 Вы включили анонимность! Теперь ваш ник спрятан!", show_alert=True)

    await call.bot.edit_message_reply_markup(chat_id=user_id,
                                             message_id=message_id,
                                             reply_markup=await start_profile_keyboard(user_id))