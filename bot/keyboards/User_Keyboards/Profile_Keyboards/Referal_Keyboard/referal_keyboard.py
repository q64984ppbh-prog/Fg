from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import db

async def forrmated_notification_referal(user_id):

    notification = await db.referals.get_referal_notification(user_id)
    if notification:
        return "🔔 Уведомление"
    else:
        return "🔕 Уведомление"

async def start_referal_keyboard(balance, user_id):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"• Забрать {balance}$ на баланс", callback_data='send_ref_money_in_balance')
            ],
            [
                InlineKeyboardButton(text="🎁 Реф. Бонус", callback_data='referal_go_bonus'),
                InlineKeyboardButton(text=await forrmated_notification_referal(user_id), callback_data='change_notification_referal')
            ],
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='start_profile')
            ]
        ]
    )
    return main

def start_bonus_referal_keyboard(balance):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"✅ Вывести {balance}$", callback_data='send_ref_bonus_in_money')
            ],
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='referal_program')
            ]
        ]
    )
    return main