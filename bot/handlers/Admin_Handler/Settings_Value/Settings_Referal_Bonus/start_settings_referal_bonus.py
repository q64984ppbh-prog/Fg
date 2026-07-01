# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

# other
from data.config import db
from utils.help_function import clean
from keyboards.Admin_Keyboards.Settings_Value_Keyboard.settings_value_key import (
    start_referal_bonus_keyboard
)

router = Router()

@router.callback_query(F.data == 'settings_bonus_referal_admin')
async def call_settings_bonus_referal_admin(call: CallbackQuery, state: FSMContext):

    await state.clear()
    user_id = call.from_user.id 
    message_id = call.message.message_id

    if not await db.admin.admin_exists(user_id):
        await call.answer()
        return
    
    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        text=clean(f"""
                                        <b>🎁 Реферальный бонус</b>

                                        <blockquote>⚙️ Здесь можно настроить наш реферальный конкурс, за который мы платим <b>{await db.admin.get_value('Amount_Bonus_Ref'):.1f}$</b> за <b>10 чел</b></blockquote>

                                        <b>ℹ️ Выберите действие</b>"""),
                                        reply_markup=start_referal_bonus_keyboard(await db.admin.get_value('Flag_Bonus_Ref')))
    
@router.callback_query(F.data == 'change_status_referal_bonus')
async def call_change_status_referal_bonus(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id
    
    if not await db.admin.admin_exists(user_id):
        await call.answer()
        return
    
    flag = await db.admin.get_value('Flag_Bonus_Ref')
    if flag == 1:
        await db.admin.update_value('Flag_Bonus_Ref', 0)
        await call.answer(text="🎁 Реферальный конкурс завершен!", show_alert=True)
    elif flag == 0:
        await db.admin.update_value('Flag_Bonus_Ref', 1)
        await call.answer(text="🎁 Мы запустили реферальный конкурс, который разорит ваш кошелек!", show_alert=True)

    await call.bot.edit_message_reply_markup(chat_id=user_id,
                                             message_id=message_id,
                                             reply_markup=start_referal_bonus_keyboard(await db.admin.get_value('Flag_Bonus_Ref')))