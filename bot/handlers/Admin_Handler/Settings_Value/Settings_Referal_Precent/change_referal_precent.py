# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, FSInputFile
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
class ChangeReferalPrecentState(StatesGroup):
    amount = State()

@router.callback_query(F.data == 'settings_referal_precent')
async def call_settings_referal_precent(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    if not await db.admin.admin_exists(user_id):
        await call.answer()
        return
    
    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        caption=clean(f"""
                                        <b>🔗 Реферальный процент</b>
                                                      
                                        <blockquote>📊 Здесь вы можете настроить реферальный процент в нашем боте!</blockquote>

                                        <b>✍🏻 Введите новый реферальный процент:</b>"""),
                                        reply_markup=back_in_meni_referal_bonus_keyboard())
    await state.set_state(ChangeReferalPrecentState.amount)

@router.message(StateFilter(ChangeReferalPrecentState.amount))
async def message_settings_ref_precent(message: Message, state: FSMContext):

    user_id = message.from_user.id 
    message_id = message.message_id

    try:
        amount = float(message.text)
    except:
        await message.bot.send_message(chat_id=user_id,
                                    caption=clean(f"""
                                    <b>🧐 Произошла ошибка!</b>

                                    <blockquote>❌ Вы ввели не верное число для <b>реферального  процент</b></blockquote>
                                     
                                    <b>✍🏻 Попробуйте еще раз:</b>"""),
                                    reply_markup=back_in_meni_referal_bonus_keyboard())
        return
    
    await db.admin.update_value('Referal_Precent', amount)
    await message.bot.send_message(chat_id=user_id,
                                 caption=clean(f"""
                                <b>✅ Значение изменено!</b>
                                
                                <blockquote>📊 Вы успешно изменили <b>реферальный процент</b></blockquote>
                                
                                <b>⬅️ Вернитесь в меню</b>"""),
                                reply_markup=back_in_meni_referal_bonus_keyboard())
    await state.clear()