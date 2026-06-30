from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def start_withdraw_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌏 Crypto Bot", callback_data='start_withdraw_cryptobot')
            ],
            [
                InlineKeyboardButton(text="⬅️ Вернуться", callback_data='start_profile')
            ]
        ]
    )
    return main

def activated_check_user_keyboard(url, amount):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"👛 Получить {amount}$", url=url)
            ]
        ]
    )
    return main

def activated_error_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️ Вернуться", callback_data='back_start')
            ]
        ]
    )
    return main

def back_in_withdraw_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️ Вернуться", callback_data='withdraw_balance')
            ]
        ]
    )
    return main

def accept_withdraw_keyboard():
    main = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='✅')
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return main

def start_withdraw_chat_keyboard(user_id, amount):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌏 Crypto Bot", callback_data=f'withdraw_chat_cryptobot_{user_id}_{amount}')
            ],
        ]
    )
    return main

def accept_withdraw_chat_keyboard(user_id, amount):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить", callback_data=f'confirm_withdraw_cryptobot_{user_id}_{amount}'),
                InlineKeyboardButton(text="❌ Отменить", callback_data=f'cancel_withdraw_cryptobot_{user_id}_{amount}')
            ],
            [
                InlineKeyboardButton(text="⬅️ Изменить метод", callback_data=f'change_method_{user_id}_{amount}')
            ],
        ]
    )
    return main