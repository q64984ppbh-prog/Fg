# main
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

# other
from data.config import db
from utils.help_function import clean
from keyboards.User_Keyboards.Profile_Keyboards.Statistick_Keyboards.Tranzaction_Keyboards.Deposit_Keyboard.deposit_key import (
    generate_deposit_keyboard,
    back_deposit_keyboard
)

router = Router()

@router.callback_query(F.data == 'tranzaction_replenishment')
async def call_tranzaction_replenishment(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id

    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        caption=clean(f"""
                                        <b>📝 История пополнений</b>

                                        <blockquote>🔎 Здесь отображается история всех ваших пополнений.</blockquote>
                                                      
                                        <b>ℹ️ Что будем делать дальше?</b>"""),
                                        reply_markup=await generate_deposit_keyboard(user_id))
    
@router.callback_query(F.data.startswith("historydeposit_"))
async def call_historydeposit_startswith(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id
    username = call.from_user.username

    data = call.data.split('_')
    deposit_id = data[1]

    date_deposit = await db.users.get_user_deposits_by_id(int(deposit_id))
    if not date_deposit:
        await call.answer("❌ Данная история депозита не найдена!", show_alert=True)
        return
    
    for dep in date_deposit:
        await call.answer()
        await call.bot.edit_message_text(chat_id=user_id,
                                            message_id=message_id,
                                            caption=clean(f"""
                                            🦋 Депозит <b>#{deposit_id}</b>

                                            <blockquote><b>{dep['system']}</b>
                                            ├ Игрок: <b>@{username}</b>
                                            ├ Айди: <b>{dep['user_id']}</b>
                                            ├ Сумма: <b>{dep['amount']}$</b>
                                            ├ Система: <b>{dep['system']}</b>
                                            └ Дата: <b>{dep['date']}</b></blockquote>

                                            <b>ℹ️ Возвращаемся в главное меню?</b>"""),
                                            reply_markup=back_deposit_keyboard())
        
@router.callback_query(lambda c: c.data.startswith("deposits_page_"))
async def paginate_deposits(callback: CallbackQuery):
    page = int(callback.data.split("_")[-1])
    keyboard = await generate_deposit_keyboard(callback.from_user.id, page=page)
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=keyboard)