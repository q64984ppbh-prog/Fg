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

@router.callback_query(F.data == 'change_notification_referal')
async def call_change_notification_referal(call: CallbackQuery):

    user_id = call.from_user.id 
    username = call.from_user.username
    message_id = call.message.message_id

    notification = await db.referals.get_referal_notification(user_id)
    if notification:
        await db.referals.change_referal_notification(user_id, False)
        await call.answer(text="🔕 Вы выключили реферальные уведомления", show_alert=True)
    else:
        await db.referals.change_referal_notification(user_id, True)
        await call.answer(text="🔔 Вы включили реферальные уведомления", show_alert=True)

    await call.bot.edit_message_reply_markup(chat_id=user_id,
                                             message_id=message_id,
                                             reply_markup=await start_referal_keyboard(await db.referals.get_referal_balance(user_id), user_id))