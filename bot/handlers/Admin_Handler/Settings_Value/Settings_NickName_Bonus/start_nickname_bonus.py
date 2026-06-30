# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

# other
from data.config import db
from utils.help_function import clean
from keyboards.Admin_Keyboards.Settings_Value_Keyboard.settings_value_key import (
    start_nickname_bonus
)

router = Router()

@router.callback_query(F.data == 'settings_bonus_pripiska_admin')
async def call_settings_bonus_pripiska_admin(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    await call.answer()
    if not await db.admin.admin_exists(user_id):
        return
    
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        caption=clean(f"""
                                        <b>🚀 Бонус за приписку</b>

                                        <blockquote>⚙️ Здесь можно настроить наш бонус за приписку в нике!</blockquote>

                                        <b>ℹ️ Выберите действие</b>"""),
                                        reply_markup=start_nickname_bonus(await db.admin.get_value('Flag_Bonus_Pripiska')))
    
@router.callback_query(F.data == 'change_status_nickname_bonus')
async def call_change_status_nickname_bonus(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id
    
    flag = await db.admin.get_value('Flag_Bonus_Pripiska')
    if flag == 1:
        await db.admin.update_value("Flag_Bonus_Pripiska", 0)
        await call.answer(caption="❌ Вы выключили конкурс!", show_alert=True)
    else:
        await db.admin.update_value("Flag_Bonus_Pripiska", 1)
        await call.answer(caption="✅ Вы включили конкурс!", show_alert=True)

    await call.bot.edit_message_reply_markup(chat_id=user_id,
                                             message_id=message_id,
                                             reply_markup=start_nickname_bonus(await db.admin.get_value('Flag_Bonus_Pripiska')))