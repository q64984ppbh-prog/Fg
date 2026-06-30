# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

# other
from data.config import db 
from utils.help_function import clean
from keyboards.User_Keyboards.Profile_Keyboards.Statistick_Keyboards.Tranzaction_Keyboards.tranzaction_key import (
    start_tranzaction_keyboard
)

router = Router()

@router.callback_query(F.data == 'tranzaction_profile')
async def call_tranzaction_profile(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id
    username = call.from_user.username

    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,   
                                        text=clean(f"""
                                        <b>🛠 Транзакции @{username}</b>
                    
                                        <b>▶️ Выберите тип транзакций для продолжения:</b>"""),
                                        reply_markup=start_tranzaction_keyboard())