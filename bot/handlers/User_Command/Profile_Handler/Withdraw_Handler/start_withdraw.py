# main
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

#other
from utils.decorators import require_subscription
from keyboards.User_Keyboards.Profile_Keyboards.Withdraw_Keyboards.withdraw_key import start_withdraw_keyboard
from utils.help_function import clean

router = Router()

@router.callback_query(F.data == 'withdraw_balance')
@require_subscription()
async def call_withdraw_balance(call: CallbackQuery, state: FSMContext):

    await state.clear()
    user_id = call.from_user.id 
    message_id = call.message.message_id

    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        text=clean(f"""
                                        <b>📤 Вывод</b> баланса
                                    
                                        <blockquote>💭 <b>Выиграл</b> — забери своё. Пусть твои победы звучат не цифрами на балансе, а звонкими монетами на счёте.</blockquote>             
                                        🦋 Выберите <b>платежную</b> систему:"""),
                                        reply_markup=start_withdraw_keyboard())