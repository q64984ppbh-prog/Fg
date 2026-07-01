# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# other
from data.config import db
from utils.help_function import clean
from keyboards.Admin_Keyboards.Settings_Value_Keyboard.settings_value_key import (
    back_in_meni_referal_bonus_keyboard
)

router = Router()
class ChangeBonusReferalSettings(StatesGroup):
    amount = State()

@router.callback_query(F.data == 'change_ref_bonus_amount')
async def call_change_ref_bonus_amount(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    if not await db.admin.admin_exists(user_id):
        await call.answer()
        return
    
    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        text=clean(f"""
                                        <b>💸 Реферальный бонус</b>
                                                      
                                        <blockquote>📊 Здесь вы можете настроить реферальный бонус в нашем боте!</blockquote>

                                        <b>✍🏻 Введите новый бонус за 10 чел:</b>"""),
                                        reply_markup=back_in_meni_referal_bonus_keyboard())
    await state.set_state(ChangeBonusReferalSettings.amount)

@router.message(StateFilter(ChangeBonusReferalSettings.amount))
async def message_settings_ref_bonus(message: Message, state: FSMContext):

    user_id = message.from_user.id 
    message_id = message.message_id

    try:
        amount = float(message.text)
    except:
        await message.bot.send_message(chat_id=user_id,
                                    text=clean(f"""
                                    <b>🧐 Произошла ошибка!</b>

                                    <blockquote>❌ Вы ввели не верное число для <b>реферального бонуса</b></blockquote>
                                     
                                    <b>✍🏻 Попробуйте еще раз:</b>"""),
                                    reply_markup=back_in_meni_referal_bonus_keyboard())
        return
    
    await db.admin.update_value('Amount_Bonus_Ref', amount)
    await message.bot.send_message(chat_id=user_id,
                                 text=clean(f"""
                                <b>✅ Значение изменено!</b>
                                
                                <blockquote>📊 Вы успешно изменили <b>реферальный бонус за 10 чел.</b></blockquote>
                                
                                <b>⬅️ Вернитесь в меню</b>"""),
                                reply_markup=back_in_meni_referal_bonus_keyboard())
    await state.clear()