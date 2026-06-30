from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_statistick_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🛠 Транзакции", callback_data='tranzaction_profile')
            ],
            [
                InlineKeyboardButton(text="⬅️ Вернуться", callback_data='start_profile')
            ]
        ]
    )
    return main

def back_statistick_keyboard():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️ Вернуться", callback_data='statistic_user')
            ]
        ]
    )
    return main