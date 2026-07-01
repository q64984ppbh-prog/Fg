# main
from aiogram import F, Router
from aiogram.types import CallbackQuery

# other
from data.config import db, username_bot_casino
from utils.help_function import clean
from utils.help_function import encode_referral
from keyboards.User_Keyboards.Profile_Keyboards.Referal_Keyboard.referal_keyboard import (
    start_referal_keyboard
)

router = Router()

@router.callback_query(F.data == 'send_ref_money_in_balance')
async def call_send_ref_money(call: CallbackQuery):

    user_id = call.from_user.id 
    message_id = call.message.message_id
    username = call.from_user.username
    balance = await db.referals.get_referal_balance(user_id)

    if balance >= await db.admin.get_value('Min_Ref_Withdraw'):
        
        await db.referals.minus_referal_balance(user_id, balance)
        await db.users.add_balance(user_id, balance)

        await call.answer(text=f"☘️ Вы вывели на свой баланс {balance:.2f}$", show_alert=True)

        balance_our = await db.referals.get_referal_balance(user_id)
        await call.bot.edit_message_text(chat_id=user_id,
                                        message_id=message_id,
                                        text=clean(f"""
                                        <b>🫂 Реферальная программа @{username}</b>
                        
                                        👤 Рефералов — <b>{await db.referals.count_referals(user_id)} чел.</b>
                                        💰 Реф. Баланс — <b>{balance_our}$</b>
                                        🕊 Заработано — <b>{await db.referals.get_referal_turnover(user_id)}$</b>
                                        
                                        <b>🛠 Ваша ссылка:</b>
                                        <code>t.me/{username_bot_casino}?start=invite_{encode_referral(user_id)}</code>"""),
                                        reply_markup=await start_referal_keyboard(balance_our, user_id))

    else:
        await call.answer(text=f"🦋 Минимальный вывод {await db.admin.get_value('Min_Ref_Withdraw'):.2f}$", show_alert=True)