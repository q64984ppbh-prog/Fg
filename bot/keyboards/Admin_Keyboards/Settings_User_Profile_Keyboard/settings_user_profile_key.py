from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def find_user_keyboard(user_id):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Баланс", callback_data=f'redact_admin_user_balance_{user_id}_plus'),
                InlineKeyboardButton(text="➖ Баланс", callback_data=f'redact_admin_user_balance_{user_id}_minus')
            ],
            [
                InlineKeyboardButton(text="👤 Убрать реферера", callback_data=f'delete_referal_user_{user_id}')
            ],
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data='admin_panel')
            ]
        ]
    )
    return main

def back_in_find_user(user_id):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Вернуться", icon_custom_emoji_id="5258236805890710909", callback_data=f'back_in_find_{user_id}')
            ]
        ]
    )
    return main

def succes_plus_balance_keyboard(username_bot_casino):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='📤 Вывести средства', url=f"http://t.me/{username_bot_casino}?start=withdraw")
            ]
        ]
    )
    return main

def succes_minus_balance_keyboard(username_bot_casino):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='📥 Пополнить средства', url=f"http://t.me/{username_bot_casino}?start=dep")
            ]
        ]
    )
    return main