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
    back_in_meni_value_keyboard
)

router = Router()
class DepositChangeState(StatesGroup):
    amount = State()

@router.callback_query(F.data.startswith("settings_deposit_admin_"))
async def call_settings_deposit_admin(call: CallbackQuery, state: FSMContext):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    if not await db.admin.admin_exists(user_id):
        await call.answer()
        return
    
    data = call.data.split('_')
    deposit_cho = data[3]

    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        caption=clean(f"""
                                        <b>{"📈 Минимальный депозит" if deposit_cho == "minimal" else "📉 Максимальный депозит"}</b>

                                        <blockquote>📊 Здесь вы можете настроить депозит в нашем боте!</blockquote>

                                        <b>{"✍🏻 Введите новый минимальный депозит" if deposit_cho == "minimal" else "✍🏻 Введите новый максимальный депозит"}</b>"""),
                                        reply_markup=back_in_meni_value_keyboard())
    await state.set_state(DepositChangeState.amount)
    await state.update_data(dep=deposit_cho)

@router.message(StateFilter(DepositChangeState.amount))
async def message_deposit_change_amount(message: Message, state: FSMContext):

    user_id = message.from_user.id 
    message_id = message.message_id

    try:
        amount = float(message.text)
    except:
        await message.bot.send_message(chat_id=user_id,
                                     caption=clean(f"""
                                    <b>🧐 Произошла ошибка!</b>
                                                   
                                    <blockquote>❌ Вы ввели не верное число для депозита</blockquote>
                                     
                                    <b>✍🏻 Попробуйте еще раз:</b>"""),
                                    reply_markup=back_in_meni_value_keyboard())
        return
    
    data = await state.get_data()
    deposit = data.get('dep')

    if deposit == 'minimal':
        await db.admin.update_value("Min_Dep", amount)
    elif deposit == 'maximal':
        await db.admin.update_value("Max_Dep", amount)

    await message.bot.send_message(chat_id=user_id,
                                 caption=clean(f"""
                                <b>✅ Значение изменено!</b>
                                
                                <blockquote>📊 Вы успешно изменили <b>{"минимальный депозит" if deposit == 'minimal' else "максимальный депозит"}</b> на <b>{amount}$</b></blockquote>
                                
                                <b>⬅️ Вернитесь в меню</b>"""),
                                reply_markup=back_in_meni_value_keyboard())
    await state.clear()
    