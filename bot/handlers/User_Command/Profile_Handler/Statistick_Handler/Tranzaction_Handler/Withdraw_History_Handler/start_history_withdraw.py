# main
from aiogram import F, Router
from aiogram.types import CallbackQuery

# other
from data.config import db
from utils.help_function import clean
from keyboards.User_Keyboards.Profile_Keyboards.Statistick_Keyboards.Tranzaction_Keyboards.Withdraw_Keyboard.withdraw_keyboards import (
    generate_withdraw_keyboard,
    back_withdraw_keyboard
)

router = Router()

@router.callback_query(F.data == 'tranzaction_withdraw')
async def call_tranzaction_withdraw(call: CallbackQuery):

    user_id = call.from_user.id
    message_id = call.message.message_id

    await call.answer()
    await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        caption=clean(f"""
                                        <b>🧾 История выводов</b>

                                        <blockquote>💰 Здесь отображается история всех ваших выводов.</blockquote>
                                                      
                                        <b>ℹ️ Что будем делать дальше?</b>"""),
                                        reply_markup=await generate_withdraw_keyboard(user_id))
    

@router.callback_query(F.data.startswith("historywithdraw_"))
async def call_historywithdraw_startswith(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id
    username = call.from_user.username

    data = call.data.split('_')
    deposit_id = data[1]

    date_deposit = await db.users.get_user_withdraw_by_id(int(deposit_id))
    if not date_deposit:
        await call.answer("❌ Данная история вывода не найдена!", show_alert=True)
        return
    
    for dep in date_deposit:
        await call.answer()
        await call.bot.edit_message_text(chat_id=user_id,
                                            message_id=message_id,
                                            caption=clean(f"""
                                            🚀 Вывод <b>#{deposit_id}</b>

                                            <blockquote><b>{dep['system']}</b>
                                            ├ Игрок: <b>@{username}</b>
                                            ├ Айди: <b>{dep['user_id']}</b>
                                            ├ Сумма: <b>{dep['amount']}$</b>
                                            ├ Система: <b>{dep['system']}</b>
                                            └ Дата: <b>{dep['date']}</b></blockquote>

                                            <b>ℹ️ Возвращаемся в главное меню?</b>"""),
                                            reply_markup=back_withdraw_keyboard())
        
@router.callback_query(lambda c: c.data.startswith("withdraw_page_"))
async def paginate_withdraw(callback: CallbackQuery):
    page = int(callback.data.split("_")[-1])
    keyboard = await generate_withdraw_keyboard(callback.from_user.id, page=page)
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=keyboard)