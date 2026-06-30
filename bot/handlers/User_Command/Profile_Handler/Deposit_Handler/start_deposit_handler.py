# main
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

# other
from utils.help_function import clean
from keyboards.User_Keyboards.Profile_Keyboards.Deposit_Keyboards.deposit_key import (
    start_deposit_keyboard
)

router = Router()

@router.callback_query(F.data == 'add_balance')
async def call_add_balance(call: CallbackQuery, state: FSMContext):

    await state.clear()
    bot = call.bot
    user_id = call.from_user.id 
    message_id = call.message.message_id

    await call.answer()
    await bot.edit_message_text(chat_id=user_id,
                                   message_id=message_id,
                                   text=clean(f"""
                                    <b>📥 Пополнение</b> баланса
                                    
                                    <blockquote>💭 <b>Большие победы</b> начинаются с маленьких пополнений.</blockquote>             
                                    🦋 Выберите <b>платежную</b> систему:"""),
                                    reply_markup=start_deposit_keyboard())