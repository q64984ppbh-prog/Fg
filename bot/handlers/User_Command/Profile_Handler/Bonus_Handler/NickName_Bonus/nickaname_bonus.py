# main
from aiogram import F, Router
from aiogram.types import CallbackQuery

# other
from data.config import db
from utils.help_function import clean
from keyboards.User_Keyboards.Profile_Keyboards.Bonus_Keyboards.bonus_keyboard import back_in_bonus_keyboard

router = Router()

@router.callback_query(F.data == 'pripiska_bonus')
async def call_nickname_bonus(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    if await db.admin.get_value('Flag_Bonus_Pripiska') == 0:
        await call.answer(caption="⚡️ Данный бонус не активен в данный момент!", show_alert=True)
        return
    
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        caption=clean(f"""
                                        <b>🍀 УТКА ПРИНОСИТ УДАЧУ!</b>
                                                      
                                        <blockquote>Поставь в свой ник <b>@duckwins и получи случайный бонус от +1% до +10%</b> к сумме своей ставке!</blockquote>
                                                      
                                        <i>Всё просто: измени ник → сделай ставку → получи повышенный выигрыш! 🚀</i>"""),
                                        reply_markup=back_in_bonus_keyboard())