# main
from aiogram import F, Router
from aiogram.types import CallbackQuery

# other
from data.config import db
from utils.help_function import clean
from keyboards.Admin_Keyboards.Settings_Value_Keyboard.settings_value_key import (
    start_value_keyboard
)

router = Router()

@router.callback_query(F.data == 'edit_value_project')
async def call_edit_value_project(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    if not await db.admin.admin_exists(user_id):
        await call.answer()
        return
    
    await call.answer()
    await call.message.delete(); await call.bot.send_message(chat_id=user_id,
                                        
                                        text=clean(f"""
                                        <b>⚙️ Раздел настройки значений</b>

                                        <blockquote>ℹ️ Здесь вы можете поменять значения в боте, начиная от депозита, до суммы бонусов</blockquote>

                                        <blockquote>📗 Мин. Деп — <b>{await db.admin.get_value('Min_Dep'):.1f}$</b>
                                        📕 Макс. Деп — <b>{await db.admin.get_value('Max_Dep'):.1f}$</b>
                                        💰 Мин. вывод — <b>{await db.admin.get_value('Min_Withdraw'):.1f}$</b>
                                        🫂 Мин. реф. Вывод — <b>{await db.admin.get_value('Min_Ref_Withdraw'):.1f}$</b>
                                        🎁 Платим за реф. бонус — <b>{await db.admin.get_value('Amount_Bonus_Ref'):.1f}$</b>
                                        👨🏻‍💻 Реф. бонус - <b>{"✅ Активен" if await db.admin.get_value('Flag_Bonus_Ref') == 1 else "❌ Не активен"}</b>
                                        🚀 Приписка бонус - <b>{"✅ Активен" if await db.admin.get_value('Flag_Bonus_Pripiska') == 1 else "❌ Не активен"}</b></blockquote>

                                        <b>👨🏻‍💻 Выберите что хотите поменять:</b>"""),
                                        reply_markup=start_value_keyboard())