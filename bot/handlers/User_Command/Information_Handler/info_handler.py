# main
from aiogram import F, Router
from aiogram.types import FSInputFile, CallbackQuery

# other
from data.config import db
from utils.help_function import clean
from keyboards.User_Keyboards.Information_Keyboards.info_key import information_keybpard

router = Router()

@router.callback_query(F.data == 'start_information')
async def call_start_information(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    await call.answer()    
    new_media = InputMediaPhoto(
        media=FSInputFile("photo/rules.jpg"),
        text=f"<b>🎁 Информация о проекте DuckWin</b>"
    )

    await call.bot.edit_message_media(
        chat_id=user_id,
        message_id=message_id,
        media=new_media,
        reply_markup=information_keybpard()
    )